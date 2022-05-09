# coding=utf-8
# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Custom application related commands"""

from __future__ import print_function

import os
from multiprocessing import Process, cpu_count
from time import time
import sys
import zipfile
import shutil
import xml.etree.ElementTree as ET
import contextlib
from knack.util import CLIError
import joblib
from joblib import Parallel, delayed
from tqdm import tqdm
from sfctl.custom_exceptions import SFCTLInternalException
from sfctl.util import get_user_confirmation

@contextlib.contextmanager
def tqdm_joblib(tqdm_object):
    """Context manager to patch joblib to report into tqdm progress bar given as argument"""
    #pylint: disable=useless-super-delegation,too-few-public-methods
    class TqdmBatchCompletionCallback(joblib.parallel.BatchCompletionCallBack):
        """
        tqdm class callback overrides to enable usage with Parallel loop
        """
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def __call__(self, *args, **kwargs):
            tqdm_object.update(n=self.batch_size)
            return super().__call__(*args, **kwargs)

    old_batch_callback = joblib.parallel.BatchCompletionCallBack
    joblib.parallel.BatchCompletionCallBack = TqdmBatchCompletionCallback
    try:
        yield tqdm_object
    finally:
        joblib.parallel.BatchCompletionCallBack = old_batch_callback
        tqdm_object.close()

def validate_app_path(app_path):
    """Validate and return application package as absolute path"""

    abspath = os.path.abspath(app_path)
    if os.path.isdir(abspath):
        return abspath

    raise ValueError(
        'Invalid path to application directory: {0}'.format(abspath)
    )

def print_progress(current, total, rel_file_path, show_progress, time_left=None):
    """Display progress for uploading"""
    if show_progress:
        print(
            '[{}/{}] files, {}'.format(current, total, rel_file_path),
            file=sys.stderr
        )
        if time_left is not None:
            print('Time left: {} seconds'.format(time_left))

def path_from_imagestore_string(imagestore_connstr):
    """
    Parse the file share path from the image store connection string
    """
    if imagestore_connstr and 'file:' in imagestore_connstr:
        conn_str_list = imagestore_connstr.split("file:")
        return conn_str_list[1]
    return False

def get_job_count():
    """
    Test-mockable wrapper for returning cpu count.
    """
    jobcount = None
    try:
        jobcount = cpu_count()
    except Exception as ex: #pylint: disable=broad-except
        print('Warning: cpu_count hit exception {}. Defaulting to 1.'.format(ex))
        jobcount = 1

    if jobcount is None:
        jobcount = 2
    return jobcount

def upload_to_fileshare(source, dest, show_progress):
    """
    Copies the package from source folder to dest folder
    """
    total_files_count = 0
    current_files_count = 0
    for root, _, files in os.walk(source):
        total_files_count += len(files)

    for root, _, files in os.walk(source):
        for single_file in files:
            rel_path = root.replace(source, '').lstrip(os.sep)
            dest_path = os.path.join(dest, rel_path)
            if not os.path.isdir(dest_path):
                os.makedirs(dest_path)

            shutil.copyfile(
                os.path.join(root, single_file), os.path.join(dest_path, single_file)
            )
            current_files_count += 1
            print_progress(current_files_count, total_files_count,
                           os.path.normpath(os.path.join(rel_path, single_file)),
                           show_progress)

    if show_progress:
        print('Complete', file=sys.stderr)

def get_timeout_left(target_timeout):
    """
    Return the number of seconds until timeout is reached, given a target_timeout which represents
      the time at which the timer should stop. If the time left is less than 0, return 0
    :param target_timeout: time measured as from epoch in seconds
    :return: int
    """
    current_time = int(time())  # time from epoch in seconds
    time_left = target_timeout - current_time

    if time_left <= 0:
        return 0
    return time_left

def get_lesser(num_a, num_b):
    """
    Return the lesser of int num_a and int num_b. If the lesser number is less than 0, return 0
    :param num_a: (int)
    :param num_b: (int)
    :return: Return the smaller of num_a or num_b.
    """

    return max(0, min(num_a, num_b))

def upload_single_file_native_imagestore(sesh, endpoint, basename, #pylint: disable=too-many-locals,too-many-arguments
                                         rel_path, single_file, root, target_timeout):
    """
    Used by upload_to_native_imagestore to upload individual files
    of the application package to cluster

    :param sesh: A requests (module) session object.
    :param endpoint: Connection url endpoint for upload requests.
    :param basename: Image store base path.
    :param rel_path: Image store relative directory path.
    :param single_file: Filename.
    :param root: Source directory path.
    :param target_timeout: Time at which timeout would be reached.
    """
    try:
        from urllib.parse import urlparse, urlencode, urlunparse
    except ImportError:
        from urllib import urlencode
        from urlparse import urlparse, urlunparse  # pylint: disable=import-error

    current_time_left = get_timeout_left(target_timeout)   # an int representing seconds

    if current_time_left == 0:
        raise SFCTLInternalException('Upload has timed out. Consider passing a longer '
                                        'timeout duration.')

    url_path = (
        os.path.normpath(os.path.join('ImageStore', basename,
                                        rel_path, single_file))
    ).replace('\\', '/')
    fp_norm = os.path.normpath(os.path.join(root, single_file))
    with open(fp_norm, 'rb') as file_opened:
        url_parsed = list(urlparse(endpoint))
        url_parsed[2] = url_path
        url_parsed[4] = urlencode(
            {'api-version': '6.1',
                'timeout': current_time_left})
        url = urlunparse(url_parsed)

        # timeout is (connect_timeout, read_timeout)
        res = sesh.put(url, data=file_opened,
                        timeout=(get_lesser(60, current_time_left), current_time_left))

        res.raise_for_status()

def upload_to_native_imagestore(sesh, endpoint, abspath, basename, #pylint: disable=too-many-locals,too-many-arguments
                                show_progress, timeout):
    """
    Upload the application package to cluster

    :param sesh: A requests (module) session object.
    :param endpoint: Connection url endpoint for upload requests.
    :param abspath: Application source path.
    :param basename: Image store destination path.
    :param show_progress: boolean to determine whether to log upload progress.
    :param timeout: Total upload timeout in seconds.
    """

    try:
        from urllib.parse import urlparse, urlencode, urlunparse
    except ImportError:
        from urllib import urlencode
        from urlparse import urlparse, urlunparse  # pylint: disable=import-error
    total_files_count = 0
    current_files_count = 0
    for root, _, files in os.walk(abspath):
        # Number of uploads is number of files plus number of directories
        total_files_count += (len(files) + 1)

    target_timeout = int(time()) + timeout
    jobcount = get_job_count()

    # Note: while we are raising some exceptions regarding upload timeout, we are leaving the
    # timeouts raised by the requests library as is since it contains enough information
    for root, _, files in os.walk(abspath):
        rel_path = os.path.normpath(os.path.relpath(root, abspath))
        filecount = len(files)

        if show_progress:
            progressdescription = 'Uploading path: {}'.format(rel_path)
            with tqdm_joblib(tqdm(desc=progressdescription, total=filecount)):
                Parallel(n_jobs=jobcount)(
                    delayed(upload_single_file_native_imagestore)(
                        sesh, endpoint, basename, rel_path, single_file, root, target_timeout)
                        for single_file in files)
        else:
            Parallel(n_jobs=jobcount)(
                delayed(upload_single_file_native_imagestore)(
                    sesh, endpoint, basename, rel_path, single_file, root, target_timeout)
                    for single_file in files)

        current_time_left = get_timeout_left(target_timeout)

        if current_time_left == 0:
            raise SFCTLInternalException('Upload has timed out. Consider passing a longer '
                                         'timeout duration.')

        url_path = (
            os.path.normpath(os.path.join('ImageStore', basename,
                                          rel_path, '_.dir'))
        ).replace('\\', '/')
        url_parsed = list(urlparse(endpoint))
        url_parsed[2] = url_path
        url_parsed[4] = urlencode({'api-version': '6.1',
                                   'timeout': current_time_left})
        url = urlunparse(url_parsed)

        res = sesh.put(url,
                       timeout=(get_lesser(60, current_time_left), current_time_left))
        res.raise_for_status()
        current_files_count += filecount + 1
        print_progress(current_files_count, total_files_count,
                       os.path.normpath(os.path.join(rel_path, '_.dir')),
                       show_progress, get_timeout_left(target_timeout))
    if show_progress:
        print('Complete', file=sys.stderr)

class IgnoreCopy():  # pylint: disable=too-few-public-methods,bad-option-value,C1001
    """
    A class which contains information and methods for the shutil.copytree method's
    callback parameter.
    """

    def __init__(self):
        # Directories which will be ignored as part of the ignore_copy function
        # If used for compressing application package:
        # A list of strings representing the abs path of the dirs in an application package
        # which need to be compressed
        # Paths in dirs_to_ignore should normalized using the _normalize_path function before setting
        self.dirs_to_ignore = []

    def ignore_copy(self, directory_being_visited, list_of_dirs):
        """
        The ignore function for shutil.copytree()

        :param directory_being_visited: str
        :param list_of_dirs: Example: ['t.txt']

        :return: a subset of the items in its second argument (must be relative path).
                 these names will then be ignored in the copy process
        """

        to_ignore = []

        for directory in list_of_dirs:

            full_path = os.path.join(directory_being_visited, directory)
            full_path = _normalize_path(full_path)
            if full_path in self.dirs_to_ignore:
                to_ignore.append(directory)

        return to_ignore

def _normalize_path(path):
    """
    Standardize a path to a file/folder location so that they can be compared

    :param path: (str) represents a path on a machine
    :return: (str) the standardized path
    """

    path = os.path.realpath(path)  # This removes slashes at the end of the path
    path = os.path.normpath(path)
    path = os.path.normcase(path)
    path = os.path.abspath(path)
    return path

# Note: provide in place compress in the future
def compress_package(app_dir, output_dir):
    """
    Compress to the location passed in (output_dir). Note that it is not the entire package
    which is compressed, but rather, only some inside parts of the app package folder.

    Check if the folder has the correct structure for a service fabric application. If
    not, raise an exception alerting user of bad folder structure.

    ZIP64 functionality is present for Python
    versions 3.4 and above.

    For example, if app_dir = C:/SomeFolder/WordCountApp
    and if output_dir = C:/SomeLocation,
    then the following will be created: C:/SomeLocation/WordCountApp

    :param app_dir: (str) An absolute path to an application package to be compressed

    :param output_dir: (str) An absolute path to the location to output the zipped dir

    :return: Nothing, or a CLIError exception
    """

    # Check if we're dealing with a dir in _check_folder_structure_and_get_dirs instead of
    # in this function

    # Normalize slashes, etc, in app_dir and output_dir
    app_dir = _normalize_path(app_dir)
    output_dir = _normalize_path(output_dir)

    compress_copy = IgnoreCopy()

    # Exception will be raised if the package isn't the correct structure
    # This list may be empty in the case of an already compressed application package
    compress_copy.dirs_to_ignore = _check_folder_structure_and_get_dirs(app_dir)

    if not compress_copy.dirs_to_ignore:
        print("Nothing to copy")

    app_name = os.path.basename(app_dir)
    copy_output_path = os.path.join(output_dir, app_name)

    # Get the relative paths under app_name of dirs_to_copy so that we know
    # where to place the new zipped file
    relative_paths_to_compress = []
    for directory in compress_copy.dirs_to_ignore:

        rel_path = directory[len(app_dir):]
        relative_paths_to_compress.append(rel_path.lstrip('\\').lstrip('/'))

    try:
        # Copy everything except the one we want to zip. Those we will do manually
        shutil.copytree(app_dir, copy_output_path, ignore=compress_copy.ignore_copy)

        i = 0
        for directory in relative_paths_to_compress:

            dir_to_compress = compress_copy.dirs_to_ignore[i]

            # Example: shutil.make_archive('C:\\Users\\user\\Downloads\\Code', 'zip',
            # root_dir='C:\\WordCountV1Original\\WordCountServicePkg\\Code')
            # The above will copy the contents of root_dir into the path given as the first
            # parameter, with a .zip extension, so that a Code.zip will be created in Downloads

            # Note for python versions before 3.4, zipping of folders larger than 2GB isn't
            # supported
            # It is more work and code to support Python 2.7 for this, and since we do plan to
            # deprecate support for Python 2.7 in the future, we will just not add it here.
            shutil.make_archive(os.path.join(copy_output_path, directory), 'zip', dir_to_compress)

            i += 1

    except zipfile.LargeZipFile as ex:
        raise CLIError('Compression failed due to file too large. If you have Python 2.7, '
                       'upgrading to 3.5 or higher will fix the issue. Please clean up '
                       'location ' + output_dir + '\n' + str(ex))

    except Exception as ex:
        raise CLIError(str.format('Compression failed due to {0}. Please clean up '
                                  'location {1}', str(ex), output_dir))


def _check_folder_structure_and_get_dirs(app_dir):
    """
    Check if the given path is a folder. If not, raise an exception indicating only
    SF app package folders can be compressed.

    Check if the folder given corresponds to a valid application structure. If the package
    is valid, return a list of dirs (abs path, normalized using the
    _normalize_path function) to be compressed.

    If the folder is already compressed, then return empty list.

    Example format:

    WordCountApp (this is the last segment of the app_dir path)

        o WordCountServicePkg
              Code
            •     WordCount.Service.exe
            •     Other Files
              Config
            •     Settings.xml
              ServiceManifest.xml

        o WordCountWebServicePkg
              Code
            •     WordCount.WebService.exe
            •     Other Files
              Config
            •     Settings.xml
              ServiceManifest.xml

        o    ApplicationManifest.xml

    The Code and Config folders should be compressed. These will be listed in the Application and Service manifests.

    :param app_dir: (str) An absolute path to an application package
    :return: A list of strings representing the absolute paths to directories which should
             be compressed. Return a CLIError if the provided path is not a dir
    """

    # Future optimization: don't copy already compressed packages. Just let the user know
    # and upload. This should be an uncommon case, and isn't worth the effort now

    to_compress = []

    if not os.path.isdir(app_dir):
        raise CLIError('Only Service Fabric application packages may be compressed. '
                       'The following path is not a directory: ' + app_dir)

    path_to_app_manifest = os.path.join(app_dir, 'ApplicationManifest.xml')

    # An application manifest file should exist directly under the directory passed in
    if not os.path.isfile(path_to_app_manifest):  # Casing does not matter
        raise CLIError('Application package to be compressed is missing ApplicationManifest.xml')

    # A list of the service packages. This should be the absolute path
    service_packages = []

    # Parse the application manifest to find which folders should have the service manifest.
    app_manifest_parsed = ET.parse(path_to_app_manifest).getroot()
    for child in app_manifest_parsed:
        # Use ends with, because the tags start with the xmlns
        if child.tag.endswith('ServiceManifestImport'):
            # We expect a child element that looks like:
            # <ServiceManifestRef ServiceManifestName="CalculatorServicePackage" ServiceManifestVersion="1.0"/>
            for inner_child in child:
                if inner_child.tag.endswith('ServiceManifestRef'):
                    path_to_service_package = os.path.join(app_dir, inner_child.attrib.get('ServiceManifestName'))
                    service_packages.append(path_to_service_package)

    # Go through each service package folder and search for the service manifest
    # The service manifest defines which packages are the code, config, and data packages, which
    # needs to be compressed.
    for service_package_path in service_packages:
        path_to_service_manifest = os.path.join(service_package_path, 'ServiceManifest.xml')

        # Raise exception is the expected service manifest file doesn't exist AND
        # if the service package isn't already zipped
        if not os.path.isfile(path_to_service_manifest) \
                and not os.path.isfile(path_to_service_manifest+'.sfpkg'):  # Casing does not matter
            raise CLIError('Service package to be compressed is missing ServiceManifest.xml in ' + service_package_path)

        service_manifest_parsed = ET.parse(path_to_service_manifest).getroot()

        for child in service_manifest_parsed:
            if child.tag.endswith('CodePackage') or \
                    child.tag.endswith('ConfigPackage') or child.tag.endswith('DataPackage'):

                # If the app package already compressed,
                # then mark a bool somewhere that says that this package is already
                # compressed, and expect that we just upload the entire package without copying to any location
                # In this case, we would not copy to output dir, and just upload. For partially compressed,
                # we should compress just those and throw the compressed in the output folder
                # For the case where there is no copy needed, we should print a statement letting the user know.

                folder_name = child.attrib.get("Name")
                folder_to_compress = os.path.join(service_package_path, folder_name)

                if not os.path.isdir(folder_to_compress):  # Casing does not matter
                    raise CLIError(str.format("{0} defined in {1} does not exist",
                                              folder_to_compress, path_to_service_manifest))

                to_compress.append(_normalize_path(folder_to_compress))

    return to_compress

def upload(path, imagestore_string='fabric:ImageStore', show_progress=False, timeout=300,  # pylint: disable=too-many-locals,missing-docstring,too-many-arguments,too-many-branches,too-many-statements
           compress=False, keep_compressed=False, compressed_location=None):

    from sfctl.config import (client_endpoint, no_verify_setting, ca_cert_info,
                              cert_info)
    import requests

    path = _normalize_path(path)
    if compressed_location is not None:
        compressed_location = _normalize_path(compressed_location)

    abspath = validate_app_path(path)
    basename = os.path.basename(abspath)

    endpoint = client_endpoint()
    cert = cert_info()
    ca_cert = True
    if no_verify_setting():
        ca_cert = False
    elif ca_cert_info():
        ca_cert = ca_cert_info()

    if all([no_verify_setting(), ca_cert_info()]):
        raise CLIError('Cannot specify both CA cert info and no verify')

    if not compress and (keep_compressed or compressed_location is not None):
        raise CLIError('--keep-compressed and --compressed-location options are only applicable '
                       'if the --compress option is set')

    compressed_pkg_location = None
    created_dir_path = None

    if compress:

        parent_folder = os.path.dirname(path)
        file_or_folder_name = os.path.basename(path)

        compressed_pkg_location = os.path.join(parent_folder, 'sfctl_compressed_temp')

        if compressed_location is not None:
            compressed_pkg_location = compressed_location

        # Check if a zip file has already been created
        created_dir_path = os.path.join(compressed_pkg_location, file_or_folder_name)

        if os.path.exists(created_dir_path):
            if get_user_confirmation(str.format('Deleting previously generated compressed files at '
                                                '{0}. If this folder has anything else, those will be '
                                                'deleted as well. Allow? ["y", "n"]: ', created_dir_path)):
                shutil.rmtree(created_dir_path)
            else:
                # We can consider adding an option to number the packages in the future.
                print('Stopping upload operation. Cannot compress to the following location '
                      'because the path already exists: ' + created_dir_path)
                return

        # Let users know where to find the compressed app package before starting the
        # copy / compression, in case the process crashes in the middle, so users
        # will know where to clean up items from, or where to upload already compressed
        # app packages from
        if show_progress:
            print('Starting package compression into location: ' + compressed_pkg_location)
            print()  # New line for formatting purposes
        compress_package(path, compressed_pkg_location)

        # Change the path to the path with the compressed package
        compressed_path = os.path.join(compressed_pkg_location, file_or_folder_name)

        # re-do validation and reset the variables
        abspath = validate_app_path(compressed_path)
        basename = os.path.basename(abspath)

    # Note: pressing ctrl + C during upload does not end the current upload in progress, but only
    # stops the next one from occurring. This will be fixed in the future.

    # Upload to either to a folder, or native image store only
    if 'file:' in imagestore_string:
        dest_path = path_from_imagestore_string(imagestore_string)

        process = Process(target=upload_to_fileshare,
                          args=(abspath, os.path.join(dest_path, basename), show_progress))

        process.start()
        process.join(timeout)  # If timeout is None then there is no timeout.

        if process.is_alive():
            process.terminate()  # This will leave any children of process orphaned.
            raise SFCTLInternalException('Upload has timed out. Consider passing a longer '
                                         'timeout duration.')

    elif imagestore_string == 'fabric:ImageStore':

        with requests.Session() as sesh:
            sesh.verify = ca_cert
            sesh.cert = cert

            # There is no need for a new process here since
            upload_to_native_imagestore(sesh, endpoint, abspath, basename, show_progress, timeout)

    else:
        raise CLIError('Unsupported image store connection string. Value should be either '
                       '"fabric:ImageStore", or start with "file:"')

    # If code has reached here, it means that upload was successful
    # To reach here, user must have agreed to clear this folder or exist the API
    # So we can safely delete the contents
    # User is expected to not create a folder by the same name during the upload duration
    # If needed, we can consider adding our content under a GUID in the future
    if compress and not keep_compressed:
        # Remove the generated files
        if show_progress:
            print('Removing generated folder ' + created_dir_path)
        shutil.rmtree(created_dir_path)

def parse_app_params(formatted_params):
    """Parse application parameters from string"""
    if formatted_params is None:
        return None

    res = []
    for k in formatted_params:
        param = {"Key": k, "Value": formatted_params[k]}
        res.append(param)

    return res

def parse_app_metrics(formatted_metrics):
    """Parse application metrics description from string"""

    if formatted_metrics is None:
        return None

    res = []

    for metric in formatted_metrics:
        metric_name = metric.get('name', None)

        if not metric_name:
            raise CLIError('Could not find required application metric name')

        maximum_capacity = metric.get('maximum_capacity', None)
        reservation_capacity = metric.get('reservation_capacity', None)
        total_application_capacity = metric.get('total_application_capacity', None)

        res.append({
            "Name": metric_name,
            "MaximumCapacity": maximum_capacity,
            "ReservationCapacity": reservation_capacity,
            "TotalApplicationCapacity": total_application_capacity})

    return res

def create(client,  # pylint: disable=too-many-locals,too-many-arguments
           app_name, app_type, app_version, parameters=None,
           min_node_count=0, max_node_count=0, metrics=None,
           timeout=60):
    """
    Creates a Service Fabric application using the specified description.
    :param str app_name: The name of the application, including the 'fabric:'
    URI scheme.
    :param str app_type: The application type name found in the application
    manifest.
    :param str app_version: The version of the application type as defined in
    the application manifest.
    :param str parameters: A JSON encoded list of application parameter
    overrides to be applied when creating the application.
    :param int min_node_count: The minimum number of nodes where Service
    Fabric will reserve capacity for this application. Note that this does not
    mean that the services of this application will be placed on all of those
    nodes.
    :param int max_node_count: The maximum number of nodes where Service
    Fabric will reserve capacity for this application. Note that this does not
    mean that the services of this application will be placed on all of those
    nodes.
    :param str metrics: A JSON encoded list of application capacity metric
    descriptions. A metric is defined as a name, associated with a set of
    capacities for each node that the application exists on.
    """

    if (any([min_node_count, max_node_count]) and
            not all([min_node_count, max_node_count])):
        raise CLIError('Must specify both maximum and minimum node count')

    if (all([min_node_count, max_node_count]) and
            min_node_count > max_node_count):
        raise CLIError('The minimum node reserve capacity count cannot '
                       'be greater than the maximum node count')

    app_params = parse_app_params(parameters)

    app_metrics = parse_app_metrics(metrics)

    app_cap_desc = {"MinimumNodes": min_node_count,
                    "MaximumNodes": max_node_count,
                    "ApplicationMetrics": app_metrics}

    app_desc = {"Name": app_name,
                "TypeName": app_type,
                "TypeVersion": app_version,
                "ParameterList": app_params,
                "ApplicationCapacity": app_cap_desc}

    client.create_application(app_desc, timeout=timeout)

def upgrade(  # pylint: disable=too-many-arguments,too-many-locals,missing-docstring
        client, application_id, application_version, parameters,
        mode="UnmonitoredAuto", replica_set_check_timeout=None,
        force_restart=None, failure_action=None,
        health_check_wait_duration="0",
        health_check_stable_duration="PT0H2M0S",
        health_check_retry_timeout="PT0H10M0S",
        upgrade_timeout="P10675199DT02H48M05.4775807S",
        upgrade_domain_timeout="P10675199DT02H48M05.4775807S",
        warning_as_error=False,
        max_unhealthy_apps=0, default_service_health_policy=None,
        service_health_policy=None, timeout=60):

    from sfctl.custom_health import (parse_service_health_policy_map,
                                     parse_service_health_policy)

    monitoring_policy = {
        "FailureAction": failure_action,
        "HealthCheckWaitDurationInMilliseconds": health_check_wait_duration,
        "HealthCheckStableDurationInMilliseconds": health_check_stable_duration,
        "healthCheckRetryTimeoutInMilliseconds": health_check_retry_timeout,
        "UpgradeTimeoutInMilliseconds": upgrade_timeout,
        "UpgradeDomainTimeoutInMilliseconds": upgrade_domain_timeout
    }

    # Must always have empty list
    app_params = parse_app_params(parameters)
    if app_params is None:
        app_params = []

    def_shp = parse_service_health_policy(default_service_health_policy)

    map_shp = parse_service_health_policy_map(service_health_policy)

    app_health_policy = {
        "ConsiderWarningAsError": warning_as_error,
        "MaxPercentUnhealthyDeployedApplications": max_unhealthy_apps,
        "DefaultServiceTypeHealthPolicy": def_shp,
        "ServiceTypeHealthPolicyMap": map_shp
    }

    desc = {
        "Name": 'fabric:/' + application_id,
        "TargetApplicationTypeVersion": application_version,
        "Parameters": app_params,
        "UpgradeKind": 'Rolling',
        "RollingUpgradeMode": mode,
        "UpgradeReplicaSetCheckTimeoutInSeconds": replica_set_check_timeout,
        "ForceRestart": force_restart,
        "MonitoringPolicy": monitoring_policy,
        "ApplicationHealthPolicy": app_health_policy}

    client.start_application_upgrade(application_id, desc, timeout=timeout)


def resume_application_upgrade(client, application_id, upgrade_domain_name, timeout=60):
    """Resumes upgrading an application in the Service Fabric cluster.
    :param str application_id: The identity of the application. This is typically the full name
    of the application without the 'fabric:' URI scheme. Starting from
    version 6.0, hierarchical names are delimited with the "~"
    character. For example, if the application name is
    "fabric:/myapp/app1", the application identity would be
    "myapp~app1" in 6.0+ and "myapp/app1" in previous versions

    :param str upgrade_domain_name: The name of the upgrade domain in which to resume the
                                       upgrade.
    """
    payload = {
        "UpgradeDomainName": upgrade_domain_name
    }

    return client.resume_application_upgrade(application_id, payload, timeout=timeout)


def delete_application(client, application_id, force_remove, timeout=60):
    """Deletes an existing Service Fabric application.

    :param str application_id: The identity of the application. This is typically the full name
    of the application without the 'fabric:' URI scheme. Starting from
    version 6.0, hierarchical names are delimited with the "~"
    character. For example, if the application name is
    "fabric:/myapp/app1", the application identity would be
    "myapp~app1" in 6.0+ and "myapp/app1" in previous versions
    :param bool force_remove: Remove a Service Fabric application or service forcefully without
    going through the graceful shutdown sequence. This parameter can
    be used to forcefully delete an application or service for which
    delete is timing out due to issues in the service code that
    prevents graceful close of replicas.
    """
    client.delete_application(application_id, force_remove=force_remove, timeout=timeout)

def get_deployed_application_info(client, application_id, node_name, include_health_state=False, timeout=60):
    """Gets the information about an application deployed on a Service Fabric node.

    This query returns system application information if the application ID provided is for system
    application. Results encompass deployed applications in active, activating, and downloading
    states. This query requires that the node name corresponds to a node on the cluster. The query
    fails if the provided node name does not point to any active Service Fabric nodes on the
    cluster.

    :param node_name: The name of the node.
    :type node_name: str
    :param application_id: The identity of the application. This is typically the full name of the
        application without the 'fabric:' URI scheme.
        Starting from version 6.0, hierarchical names are delimited with the "~" character.
        For example, if the application name is "fabric:/myapp/app1", the application identity would
        be "myapp~app1" in 6.0+ and "myapp/app1" in previous versions.
    :type application_id: str
    :param timeout: The server timeout for performing the operation in seconds. This timeout
        specifies the time duration that the client is willing to wait for the requested operation to
        complete. The default value for this parameter is 60 seconds. Default value is 60.
    :paramtype timeout: long
    :param include_health_state: Include the health state of an entity.
        If this parameter is false or not specified, then the health state returned is "Unknown".
        When set to true, the query goes in parallel to the node and the health system service before
        the results are merged.
        As a result, the query is more expensive and may take a longer time. Default value is False.
    :paramtype include_health_state: bool
    """

    return client.get_deployed_application_info(node_name, application_id, include_health_state=include_health_state, timeout=timeout)


def get_deployed_application_info_list(client, node_name, include_health_state=False, continuation_token=None, max_results=0, timeout=60):
    """Gets the list of applications deployed on a Service Fabric node.

    Gets the list of applications deployed on a Service Fabric node. The results do not include
    information about deployed system applications unless explicitly queried for by ID. Results
    encompass deployed applications in active, activating, and downloading states. This query
    requires that the node name corresponds to a node on the cluster. The query fails if the
    provided node name does not point to any active Service Fabric nodes on the cluster.

    :param node_name: The name of the node.
    :type node_name: str
    :keyword timeout: The server timeout for performing the operation in seconds. This timeout
        specifies the time duration that the client is willing to wait for the requested operation to
        complete. The default value for this parameter is 60 seconds. Default value is 60.
    :paramtype timeout: long
    :param include_health_state: Include the health state of an entity.
        If this parameter is false or not specified, then the health state returned is "Unknown".
        When set to true, the query goes in parallel to the node and the health system service before
        the results are merged.
        As a result, the query is more expensive and may take a longer time. Default value is False.
    :paramtype include_health_state: bool
    :param continuation_token: The continuation token parameter is used to obtain next
        set of results. A continuation token with a non-empty value is included in the response of the
        API when the results from the system do not fit in a single response. When this value is passed
        to the next API call, the API returns next set of results. If there are no further results,
        then the continuation token does not contain a value. The value of this parameter should not be
        URL encoded. Default value is None.
    :param max_results: The maximum number of results to be returned as part of the paged
        queries. This parameter defines the upper bound on the number of results returned. The results
        returned can be less than the specified maximum results if they do not fit in the message as
        per the max message size restrictions defined in the configuration. If this parameter is zero
        or not specified, the paged query includes as many results as possible that fit in the return
        """

    return client.get_deployed_application_info_list(node_name, include_health_state=include_health_state, continuation_token_parameter=continuation_token,
                                                    max_results=max_results, timeout=timeout)


def get_deployed_application_health(client, application_id, node_name, deployed_service_packages_health_state_filter=0,
                                    events_health_state_filter=0, exclude_health_statistics=False, timeout=60):
    """Gets the information about health of an application deployed on a Service Fabric node.

        Gets the information about health of an application deployed on a Service Fabric node. Use
        EventsHealthStateFilter to optionally filter for the collection of HealthEvent objects reported
        on the deployed application based on health state. Use DeployedServicePackagesHealthStateFilter
        to optionally filter for DeployedServicePackageHealth children based on health state.

        :param node_name: The name of the node.
        :type node_name: str
        :param application_id: The identity of the application. This is typically the full name of the
         application without the 'fabric:' URI scheme.
         Starting from version 6.0, hierarchical names are delimited with the "~" character.
         For example, if the application name is "fabric:/myapp/app1", the application identity would
         be "myapp~app1" in 6.0+ and "myapp/app1" in previous versions.
        :type application_id: str
        :param events_health_state_filter: Allows filtering the collection of HealthEvent objects
         returned based on health state.
         The possible values for this parameter include integer value of one of the following health
         states.
         Only events that match the filter are returned. All events are used to evaluate the aggregated
         health state.
         If not specified, all entries are returned. The state values are flag-based enumeration, so
         the value could be a combination of these values, obtained using the bitwise 'OR' operator. For
         example, If the provided value is 6 then all of the events with HealthState value of OK (2) and
         Warning (4) are returned
         * Default - Default value. Matches any HealthState. The value is zero.
         * None - Filter that doesn't match any HealthState value. Used in order to return no results
         on a given collection of states. The value is 1.
         * Ok - Filter that matches input with HealthState value Ok. The value is 2.
         * Warning - Filter that matches input with HealthState value Warning. The value is 4.
         * Error - Filter that matches input with HealthState value Error. The value is 8.
         * All - Filter that matches input with any HealthState value. The value is 65535. Default
         value is 0.
        :paramtype events_health_state_filter: int
        :param deployed_service_packages_health_state_filter: Allows filtering of the deployed
         service package health state objects returned in the result of deployed application health
         query based on their health state.
         The possible values for this parameter include integer value of one of the following health
         states.
         Only deployed service packages that match the filter are returned. All deployed service
         packages are used to evaluate the aggregated health state of the deployed application.
         If not specified, all entries are returned.
         The state values are flag-based enumeration, so the value can be a combination of these
         values, obtained using the bitwise 'OR' operator.
         For example, if the provided value is 6 then health state of service packages with HealthState
         value of OK (2) and Warning (4) are returned.
         * Default - Default value. Matches any HealthState. The value is zero.
         * None - Filter that doesn't match any HealthState value. Used in order to return no results
         on a given collection of states. The value is 1.
         * Ok - Filter that matches input with HealthState value Ok. The value is 2.
         * Warning - Filter that matches input with HealthState value Warning. The value is 4.
         * Error - Filter that matches input with HealthState value Error. The value is 8.
         * All - Filter that matches input with any HealthState value. The value is 65535. Default
         value is 0.
        :paramtype deployed_service_packages_health_state_filter: int
        :param exclude_health_statistics: Indicates whether the health statistics should be returned
         as part of the query result. False by default.
         The statistics show the number of children entities in health state Ok, Warning, and Error.
         Default value is False.
        :paramtype exclude_health_statistics: bool
        :param timeout: The server timeout for performing the operation in seconds. This timeout
         specifies the time duration that the client is willing to wait for the requested operation to
         complete. The default value for this parameter is 60 seconds. Default value is 60.
        """

    return client.get_deployed_application_health(node_name, application_id, events_health_state_filter=events_health_state_filter, 
                                            deployed_service_packages_health_state_filter=deployed_service_packages_health_state_filter,
                                            exclude_health_statistics=exclude_health_statistics, timeout=timeout)

def get_application_info(client, application_id, exclude_application_parameters=False, timeout=60):
    """Gets information about a Service Fabric application.

        Returns the information about the application that was created or in the process of being
        created in the Service Fabric cluster and whose name matches the one specified as the
        parameter. The response includes the name, type, status, parameters, and other details about
        the application.

        :param application_id: The identity of the application. This is typically the full name of the
            application without the 'fabric:' URI scheme.
            Starting from version 6.0, hierarchical names are delimited with the "~" character.
            For example, if the application name is "fabric:/myapp/app1", the application identity would
            be "myapp~app1" in 6.0+ and "myapp/app1" in previous versions.
        :type application_id: str
        :param exclude_application_parameters: The flag that specifies whether application parameters
            will be excluded from the result. Default value is False.
        :paramtype exclude_application_parameters: bool
        """
    return client.get_application_info(application_id, exclude_application_parameters=exclude_application_parameters, timeout=timeout)

def get_application_info_list(client, application_definition_kind_filter=0, application_type_name=None, exclude_application_parameters=False,
                              continuation_token = None, max_results=0, timeout=60):
    """Gets the list of applications created in the Service Fabric cluster that match the specified
    filters.

    Gets the information about the applications that were created or in the process of being
    created in the Service Fabric cluster and match the specified filters. The response includes
    the name, type, status, parameters, and other details about the application. If the
    applications do not fit in a page, one page of results is returned as well as a continuation
    token, which can be used to get the next page. Filters ApplicationTypeName and
    ApplicationDefinitionKindFilter cannot be specified at the same time.

    :param application_definition_kind_filter: Used to filter on ApplicationDefinitionKind, which
        is the mechanism used to define a Service Fabric application.


        * Default - Default value, which performs the same function as selecting "All". The value is
        0.
        * All - Filter that matches input with any ApplicationDefinitionKind value. The value is
        65535.
        * ServiceFabricApplicationDescription - Filter that matches input with
        ApplicationDefinitionKind value ServiceFabricApplicationDescription. The value is 1.
        * Compose - Filter that matches input with ApplicationDefinitionKind value Compose. The value
        is 2. Default value is 0.
    :paramtype application_definition_kind_filter: int
    :param application_type_name: The application type name used to filter the applications to
        query for. This value should not contain the application type version. Default value is None.
    :paramtype application_type_name: str
    :param exclude_application_parameters: The flag that specifies whether application parameters
        will be excluded from the result. Default value is False.
    :paramtype exclude_application_parameters: bool
    :param continuation_token: The continuation token parameter is used to obtain next
        set of results. A continuation token with a non-empty value is included in the response of the
        API when the results from the system do not fit in a single response. When this value is passed
        to the next API call, the API returns next set of results. If there are no further results,
        then the continuation token does not contain a value. The value of this parameter should not be
        URL encoded. Default value is None.
    :paramtype continuation_token: str
    :param max_results: The maximum number of results to be returned as part of the paged
        queries. This parameter defines the upper bound on the number of results returned. The results
        returned can be less than the specified maximum results if they do not fit in the message as
        per the max message size restrictions defined in the configuration. If this parameter is zero
        or not specified, the paged query includes as many results as possible that fit in the return
        message. Default value is 0.
        """
    return client.get_application_info_list(application_definition_kind_filter=application_definition_kind_filter,
                                            application_type_name=application_type_name,
                                            exclude_application_parameters=exclude_application_parameters,
                                            continuation_token_parameter=continuation_token, max_results=max_results, timeout=timeout)

def get_application_type_info_list_by_name(client, application_type_name, application_type_version=None, 
                                            exclude_application_parameters=False, continuation_token=None, max_results=0, timeout=60):
    """Gets the list of application types in the Service Fabric cluster matching exactly the specified
        name.

        Returns the information about the application types that are provisioned or in the process of
        being provisioned in the Service Fabric cluster. These results are of application types whose
        name match exactly the one specified as the parameter, and which comply with the given query
        parameters. All versions of the application type matching the application type name are
        returned, with each version returned as one application type. The response includes the name,
        version, status, and other details about the application type. This is a paged query, meaning
        that if not all of the application types fit in a page, one page of results is returned as well
        as a continuation token, which can be used to get the next page. For example, if there are 10
        application types but a page only fits the first three application types, or if max results is
        set to 3, then three is returned. To access the rest of the results, retrieve subsequent pages
        by using the returned continuation token in the next query. An empty continuation token is
        returned if there are no subsequent pages.

        :param application_type_name: The name of the application type.
        :type application_type_name: str
        :param application_type_version: The version of the application type. Default value is None.
        :paramtype application_type_version: str
        :param exclude_application_parameters: The flag that specifies whether application parameters
         will be excluded from the result. Default value is False.
        :paramtype exclude_application_parameters: bool
        :param continuation_token: The continuation token parameter is used to obtain next
         set of results. A continuation token with a non-empty value is included in the response of the
         API when the results from the system do not fit in a single response. When this value is passed
         to the next API call, the API returns next set of results. If there are no further results,
         then the continuation token does not contain a value. The value of this parameter should not be
         URL encoded. Default value is None.
        :paramtype continuation_token_parameter: str
        :param max_results: The maximum number of results to be returned as part of the paged
         queries. This parameter defines the upper bound on the number of results returned. The results
         returned can be less than the specified maximum results if they do not fit in the message as
         per the max message size restrictions defined in the configuration. If this parameter is zero
         or not specified, the paged query includes as many results as possible that fit in the return
         message. Default value is 0.
        :paramtype max_results: long
        """
    return client.get_application_type_info_list_by_name(application_type_name, application_type_version=application_type_version,
                                                  exclude_application_parameters=exclude_application_parameters, continuation_token_paramater=continuation_token,
                                                  max_results=max_results, timeout=timeout)

def get_application_type_info_list(client, application_type_definition_kind_filter=0, exclude_application_parameters=False,
                                    continuation_token=None, max_results=0, timeout=60):
    """Gets the list of application types in the Service Fabric cluster.

    Returns the information about the application types that are provisioned or in the process of
    being provisioned in the Service Fabric cluster. Each version of an application type is
    returned as one application type. The response includes the name, version, status, and other
    details about the application type. This is a paged query, meaning that if not all of the
    application types fit in a page, one page of results is returned as well as a continuation
    token, which can be used to get the next page. For example, if there are 10 application types
    but a page only fits the first three application types, or if max results is set to 3, then
    three is returned. To access the rest of the results, retrieve subsequent pages by using the
    returned continuation token in the next query. An empty continuation token is returned if there
    are no subsequent pages.

    :param application_type_definition_kind_filter: Used to filter on
        ApplicationTypeDefinitionKind which is the mechanism used to define a Service Fabric
        application type.


        * Default - Default value, which performs the same function as selecting "All". The value is
        0.
        * All - Filter that matches input with any ApplicationTypeDefinitionKind value. The value is
        65535.
        * ServiceFabricApplicationPackage - Filter that matches input with
        ApplicationTypeDefinitionKind value ServiceFabricApplicationPackage. The value is 1.
        * Compose - Filter that matches input with ApplicationTypeDefinitionKind value Compose. The
        value is 2. Default value is 0.
    :paramtype application_type_definition_kind_filter: int
    :param exclude_application_parameters: The flag that specifies whether application parameters
        will be excluded from the result. Default value is False.
    :paramtype exclude_application_parameters: bool
    :param continuation_token: The continuation token parameter is used to obtain next
        set of results. A continuation token with a non-empty value is included in the response of the
        API when the results from the system do not fit in a single response. When this value is passed
        to the next API call, the API returns next set of results. If there are no further results,
        then the continuation token does not contain a value. The value of this parameter should not be
        URL encoded. Default value is None.
    :paramtype continuation_token_parameter: str
    :param max_results: The maximum number of results to be returned as part of the paged
        queries. This parameter defines the upper bound on the number of results returned. The results
        returned can be less than the specified maximum results if they do not fit in the message as
        per the max message size restrictions defined in the configuration. If this parameter is zero
        or not specified, the paged query includes as many results as possible that fit in the return
        message. Default value is 0.
        """
    return client.get_application_type_info_list(application_type_definition_kind_filter=application_type_definition_kind_filter,
                                          exclude_application_parameters=exclude_application_parameters, continuation_token_paramater=continuation_token,
                                          max_results=max_results, timeout=timeout)


def get_application_health(client, application_id, events_health_state_filter=0,  services_health_state_filter=0,
                            deployed_applications_health_state_filter=0, exclude_health_statistics=False, timeout=60):
    """Gets the health of the service fabric application.

    Returns the heath state of the service fabric application. The response reports either Ok,
    Error or Warning health state. If the entity is not found in the health store, it will return
    Error.

    :param application_id: The identity of the application. This is typically the full name of the
        application without the 'fabric:' URI scheme.
        Starting from version 6.0, hierarchical names are delimited with the "~" character.
        For example, if the application name is "fabric:/myapp/app1", the application identity would
        be "myapp~app1" in 6.0+ and "myapp/app1" in previous versions.
    :type application_id: str
    :param events_health_state_filter: Allows filtering the collection of HealthEvent objects
        returned based on health state.
        The possible values for this parameter include integer value of one of the following health
        states.
        Only events that match the filter are returned. All events are used to evaluate the aggregated
        health state.
        If not specified, all entries are returned. The state values are flag-based enumeration, so
        the value could be a combination of these values, obtained using the bitwise 'OR' operator. For
        example, If the provided value is 6 then all of the events with HealthState value of OK (2) and
        Warning (4) are returned.


        * Default - Default value. Matches any HealthState. The value is zero.
        * None - Filter that doesn't match any HealthState value. Used in order to return no results
        on a given collection of states. The value is 1.
        * Ok - Filter that matches input with HealthState value Ok. The value is 2.
        * Warning - Filter that matches input with HealthState value Warning. The value is 4.
        * Error - Filter that matches input with HealthState value Error. The value is 8.
        * All - Filter that matches input with any HealthState value. The value is 65535. Default
        value is 0.
    :paramtype events_health_state_filter: int
    :param deployed_applications_health_state_filter: Allows filtering of the deployed
        applications health state objects returned in the result of application health query based on
        their health state.
        The possible values for this parameter include integer value of one of the following health
        states. Only deployed applications that match the filter will be returned.
        All deployed applications are used to evaluate the aggregated health state. If not specified,
        all entries are returned.
        The state values are flag-based enumeration, so the value could be a combination of these
        values, obtained using bitwise 'OR' operator.
        For example, if the provided value is 6 then health state of deployed applications with
        HealthState value of OK (2) and Warning (4) are returned.


        * Default - Default value. Matches any HealthState. The value is zero.
        * None - Filter that doesn't match any HealthState value. Used in order to return no results
        on a given collection of states. The value is 1.
        * Ok - Filter that matches input with HealthState value Ok. The value is 2.
        * Warning - Filter that matches input with HealthState value Warning. The value is 4.
        * Error - Filter that matches input with HealthState value Error. The value is 8.
        * All - Filter that matches input with any HealthState value. The value is 65535. Default
        value is 0.
    :paramtype deployed_applications_health_state_filter: int
    :param services_health_state_filter: Allows filtering of the services health state objects
        returned in the result of services health query based on their health state.
        The possible values for this parameter include integer value of one of the following health
        states.
        Only services that match the filter are returned. All services are used to evaluate the
        aggregated health state.
        If not specified, all entries are returned. The state values are flag-based enumeration, so
        the value could be a combination of these values,
        obtained using bitwise 'OR' operator. For example, if the provided value is 6 then health
        state of services with HealthState value of OK (2) and Warning (4) will be returned.


        * Default - Default value. Matches any HealthState. The value is zero.
        * None - Filter that doesn't match any HealthState value. Used in order to return no results
        on a given collection of states. The value is 1.
        * Ok - Filter that matches input with HealthState value Ok. The value is 2.
        * Warning - Filter that matches input with HealthState value Warning. The value is 4.
        * Error - Filter that matches input with HealthState value Error. The value is 8.
        * All - Filter that matches input with any HealthState value. The value is 65535. Default
        value is 0.
    :paramtype services_health_state_filter: int
    :param exclude_health_statistics: Indicates whether the health statistics should be returned
        as part of the query result. False by default.
        The statistics show the number of children entities in health state Ok, Warning, and Error.
        Default value is False.
    :paramtype exclude_health_statistics: bool
    """
    return client.get_application_health(application_id, events_health_state_filter=events_health_state_filter, services_health_state_filter=services_health_state_filter,
                                         deployed_applications_health_state_filter=deployed_applications_health_state_filter, exclude_health_statistics=exclude_health_statistics, timeout=timeout)

def get_application_manifest(client, application_type_name, application_type_version, timeout=60):
    """Gets the manifest describing an application type.
    The response contains the application manifest XML as a string.

    :param application_type_name: The name of the application type.
    :type application_type_name: str
    :param application_type_version: The version of the application type.
    :paramtype application_type_version: str
    """
    return client.get_application_manifest(application_type_name, application_type_version=application_type_version, timeout=timeout)
