# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Custom application related commands"""

from __future__ import print_function

import os
import sys
import shutil
from knack.util import CLIError

def validate_app_path(app_path):
    """Validate and return application package as absolute path"""

    abspath = os.path.abspath(app_path)
    if os.path.isdir(abspath):
        return abspath
    else:
        raise ValueError(
            'Invalid path to application directory: {0}'.format(abspath)
        )

def print_progress(current, total, rel_file_path, show_progress):
    """Display progress for uploading"""
    if show_progress:
        print(
            '[{}/{}] files, {}'.format(current, total, rel_file_path),
            file=sys.stderr
        )

def path_from_imagestore_string(imagestore_connstr):
    """
    Parse the file share path from the image store connection string
    """
    if imagestore_connstr and 'file:' in imagestore_connstr:
        conn_str_list = imagestore_connstr.split("file:")
        return conn_str_list[1]
    return False

def upload_to_fileshare(source, dest, show_progress):
    """
    Copies the package from source folder to dest folder
    """
    total_files_count = 0
    current_files_count = 0
    for root, _, files in os.walk(source):
        total_files_count += len(files)

    for root, _, files in os.walk(source):
        for f in files:
            rel_path = root.replace(source, '').lstrip(os.sep)
            dest_path = os.path.join(dest, rel_path)
            if not os.path.isdir(dest_path):
                os.makedirs(dest_path)

            shutil.copyfile(
                os.path.join(root, f), os.path.join(dest_path, f)
            )
            current_files_count += 1
            print_progress(current_files_count, total_files_count,
                           os.path.normpath(os.path.join(rel_path, f)),
                           show_progress)

    if show_progress:
        print('Complete', file=sys.stderr)

def upload_to_native_imagestore(sesh, endpoint, abspath, basename, #pylint: disable=too-many-locals
                                show_progress):
    """
    Upload the application package to cluster
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

    for root, _, files in os.walk(abspath):
        rel_path = os.path.normpath(os.path.relpath(root, abspath))
        for f in files:
            url_path = (
                os.path.normpath(os.path.join('ImageStore', basename,
                                              rel_path, f))
            ).replace('\\', '/')
            fp_norm = os.path.normpath(os.path.join(root, f))
            with open(fp_norm, 'rb') as file_opened:
                url_parsed = list(urlparse(endpoint))
                url_parsed[2] = url_path
                url_parsed[4] = urlencode(
                    {'api-version': '3.0-preview'})
                url = urlunparse(url_parsed)
                res = sesh.put(url, data=file_opened)
                res.raise_for_status()
                current_files_count += 1
                print_progress(current_files_count, total_files_count,
                               os.path.normpath(os.path.join(rel_path, f)),
                               show_progress)
        url_path = (
            os.path.normpath(os.path.join('ImageStore', basename,
                                          rel_path, '_.dir'))
        ).replace('\\', '/')
        url_parsed = list(urlparse(endpoint))
        url_parsed[2] = url_path
        url_parsed[4] = urlencode({'api-version': '3.0-preview'})
        url = urlunparse(url_parsed)
        res = sesh.put(url)
        res.raise_for_status()
        current_files_count += 1
        print_progress(current_files_count, total_files_count,
                       os.path.normpath(os.path.join(rel_path, '_.dir')),
                       show_progress)
    if show_progress:
        print('Complete', file=sys.stderr)

def upload(path, imagestore_string='fabric:ImageStore', show_progress=False):  # pylint: disable=too-many-locals,missing-docstring
    from sfctl.config import (client_endpoint, no_verify_setting, ca_cert_info,
                              cert_info)
    import requests

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


    # Upload to either to a folder, or native image store only
    if 'file:' in imagestore_string:
        dest_path = path_from_imagestore_string(imagestore_string)
        upload_to_fileshare(abspath, os.path.join(dest_path, basename),
                            show_progress)
    elif imagestore_string == 'fabric:ImageStore':
        with requests.Session() as sesh:
            sesh.verify = ca_cert
            sesh.cert = cert
            upload_to_native_imagestore(sesh, endpoint, abspath, basename,
                                        show_progress)
    else:
        raise CLIError('Unsupported image store connection string')

def parse_app_params(formatted_params):
    """Parse application parameters from string"""
    from azure.servicefabric.models.application_parameter import (
        ApplicationParameter
    )

    if formatted_params is None:
        return None

    res = []
    for k in formatted_params:
        param = ApplicationParameter(k, formatted_params[k])
        res.append(param)

    return res

def parse_app_metrics(formatted_metrics):
    """Parse application metrics description from string"""
    from azure.servicefabric.models.application_metric_description import (
        ApplicationMetricDescription
    )

    if formatted_metrics is None:
        return None

    res = []
    for metric in formatted_metrics:
        metric_name = metric.get('name', None)
        if not metric_name:
            raise CLIError('Could not find required application metric name')

        metric_max_cap = metric.get('maximum_capacity', None)
        metric_reserve_cap = metric.get('reservation_capacity', None)
        metric_total_cap = metric.get('total_application_capacity', None)
        metric_desc = ApplicationMetricDescription(metric_name, metric_max_cap,
                                                   metric_reserve_cap,
                                                   metric_total_cap)
        res.append(metric_desc)
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
    from azure.servicefabric.models.application_description import (
        ApplicationDescription
    )
    from azure.servicefabric.models.application_capacity_description import (
        ApplicationCapacityDescription
    )

    if (any([min_node_count, max_node_count]) and
            not all([min_node_count, max_node_count])):
        raise CLIError('Must specify both maximum and minimum node count')

    if (all([min_node_count, max_node_count]) and
            min_node_count > max_node_count):
        raise CLIError('The minimum node reserve capacity count cannot '
                       'be greater than the maximum node count')

    app_params = parse_app_params(parameters)

    app_metrics = parse_app_metrics(metrics)

    app_cap_desc = ApplicationCapacityDescription(min_node_count,
                                                  max_node_count,
                                                  app_metrics)

    app_desc = ApplicationDescription(app_name, app_type, app_version,
                                      app_params, app_cap_desc)

    client.create_application(app_desc, timeout)

def upgrade(  # pylint: disable=too-many-arguments,too-many-locals,missing-docstring
        client, app_id, app_version, parameters, mode="UnmonitoredAuto",
        replica_set_check_timeout=None, force_restart=None,
        failure_action=None, health_check_wait_duration="0",
        health_check_stable_duration="PT0H2M0S",
        health_check_retry_timeout="PT0H10M0S",
        upgrade_timeout="P10675199DT02H48M05.4775807S",
        upgrade_domain_timeout="P10675199DT02H48M05.4775807S",
        warning_as_error=False,
        max_unhealthy_apps=0, default_service_health_policy=None,
        service_health_policy=None, timeout=60):
    from azure.servicefabric.models.application_upgrade_description import (
        ApplicationUpgradeDescription
    )
    from azure.servicefabric.models.monitoring_policy_description import (
        MonitoringPolicyDescription
    )
    from azure.servicefabric.models.application_health_policy import (
        ApplicationHealthPolicy
    )
    from sfctl.custom_health import (parse_service_health_policy_map,
                                     parse_service_health_policy)

    monitoring_policy = MonitoringPolicyDescription(
        failure_action, health_check_wait_duration,
        health_check_stable_duration, health_check_retry_timeout,
        upgrade_timeout, upgrade_domain_timeout
    )

    # Must always have empty list
    app_params = parse_app_params(parameters)
    if app_params is None:
        app_params = []

    def_shp = parse_service_health_policy(default_service_health_policy)

    map_shp = parse_service_health_policy_map(service_health_policy)

    app_health_policy = ApplicationHealthPolicy(warning_as_error,
                                                max_unhealthy_apps, def_shp,
                                                map_shp)

    desc = ApplicationUpgradeDescription(app_id, app_version, app_params,
                                         "Rolling", mode,
                                         replica_set_check_timeout,
                                         force_restart, monitoring_policy,
                                         app_health_policy)

    client.start_application_upgrade(app_id, desc, timeout)
