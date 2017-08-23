# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Custom application related commands"""

from __future__ import print_function

import os
import sys
from knack.util import CLIError

def create_compose_application(client, compose_file, application_id,
                               repo_user=None, encrypted=False,
                               repo_pass=None, timeout=60):
    """
    Creates a Service Fabric application from a Compose file
    :param str application_id:  The id of application to create from
    Compose file. This is typically the full id of the application
    including "fabric:" URI scheme
    :param str compose_file: Path to the Compose file to use
    :param str repo_user: Container repository user name if needed for
    authentication
    :param bool encrypted: If true, indicate to use an encrypted password
    rather than prompting for a plaintext one
    :param str repo_pass: Encrypted container repository password
    """
    from azure.servicefabric.models.create_compose_application_description import CreateComposeApplicationDescription # pylint: disable=line-too-long
    from azure.servicefabric.models.repository_credential import (
        RepositoryCredential
    )
    from getpass import getpass

    if (any([encrypted, repo_pass]) and
            not all([encrypted, repo_pass, repo_user])):
        raise CLIError('Invalid credentials syntax')

    if repo_user and not repo_pass:
        repo_pass = getpass('Repository password: ')

    repo_cred = RepositoryCredential(repo_user, repo_pass, encrypted)

    file_contents = None
    with open(compose_file) as f_desc:
        file_contents = f_desc.read()
    if not file_contents:
        raise CLIError('Could not read {}'.format(compose_file))

    model = CreateComposeApplicationDescription(application_id, file_contents,
                                                repo_cred)

    client.create_compose_application(model, timeout)


def validate_app_path(app_path):
    """Validate and return application package as absolute path"""

    abspath = os.path.abspath(app_path)
    if os.path.isdir(abspath):
        return abspath
    else:
        raise ValueError(
            'Invalid path to application directory: {0}'.format(abspath)
        )


def upload(path, show_progress=False):  # pylint: disable=too-many-locals
    """
    Copies a Service Fabric application package to the image store.
    The cmdlet copies a Service Fabric application package to the image store.
    After copying the application package, use the sf application provision
    cmdlet to register the application type.
    Can optionally display upload progress for each file in the package.
    Upload progress is sent to `stderr`.
    :param str path: The path to your local application package
    :param bool show_progress: Show file upload progress
    """
    from sfctl.config import (client_endpoint, no_verify_setting, ca_cert_info,
                              cert_info)
    from getpass import getpass

    try:
        from urllib.parse import urlparse, urlencode, urlunparse
    except ImportError:
        from urllib import urlencode
        from urlparse import urlparse, urlunparse  # pylint: disable=import-error
    import requests

    abspath = validate_app_path(path)
    basename = os.path.basename(abspath)

    endpoint = client_endpoint()
    cert = cert_info()
    if cert:
        # As a workaround we prompt for password input here, then store the
        # password in memory. This is required as Service Fabric appears to
        # terminate connections early, thus requiring multiple password inputs
        # otherwise
        class PasswordContext(requests.packages.urllib3.contrib.pyopenssl.OpenSSL.SSL.Context): #pylint: disable=line-too-long,no-member,too-few-public-methods
            """Custom password context for handling x509 passphrases"""
            def __init__(self, method):
                super(PasswordContext, self).__init__(method)
                self.passphrase = None

                def passwd_cb(maxlen, prompt_twice, userdata):
                    """Password retrival callback"""
                    if self.passphrase is None:
                        self.passphrase = getpass('Enter cert pass phrase: ')
                        if not isinstance(self.passphrase, bytes):
                            self.passphrase = str.encode(self.passphrase)
                    if len(self.passphrase) < maxlen:
                        return self.passphrase
                    return ''
                self.set_passwd_cb(passwd_cb)

        # Monkey-patch the subclass into OpenSSL.SSL so it is used in place of
        # the stock version
        requests.packages.urllib3.contrib.pyopenssl.OpenSSL.SSL.Context = PasswordContext #pylint: disable=line-too-long,no-member

    ca_cert = True
    if no_verify_setting():
        ca_cert = False
    elif ca_cert_info():
        ca_cert = ca_cert_info()

    if all([no_verify_setting(), ca_cert_info()]):
        raise CLIError('Cannot specify both CA cert info and no verify')

    with requests.Session() as sesh:
        sesh.verify = ca_cert
        sesh.cert = cert

        total_files_count = 0
        current_files_count = 0
        total_files_size = 0
        current_files_size = {'size': 0}

        for root, _, files in os.walk(abspath):
            total_files_count += (len(files) + 1)
            for f in files:
                t_stat = os.stat(os.path.join(root, f))
                total_files_size += t_stat.st_size

        def print_progress(size, rel_file_path):
            """Display progress for uploading"""
            current_files_size['size'] += size
            if show_progress:
                print(
                    '[{}/{}] files, [{}/{}] bytes, {}'.format(
                        current_files_count,
                        total_files_count,
                        current_files_size["size"],
                        total_files_size,
                        rel_file_path), file=sys.stderr)

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

                    def file_chunk(target_file, rel_path, print_progress):
                        """Yield partial chunks of file contents"""
                        chunk = True
                        while chunk:
                            chunk = target_file.read(100000)
                            print_progress(len(chunk), rel_path)
                            yield chunk

                    fc_iter = file_chunk(file_opened, os.path.normpath(
                        os.path.join(rel_path, f)), print_progress)
                    # Cannot check this response until issue 15 gets fixed,
                    # successful file uploads result in a 400 error response
                    sesh.put(url, data=fc_iter)
                    current_files_count += 1
                    print_progress(0, os.path.normpath(
                        os.path.join(rel_path, f)
                    ))
            url_path = (
                os.path.normpath(os.path.join('ImageStore', basename,
                                              rel_path, '_.dir'))
            ).replace('\\', '/')
            url_parsed = list(urlparse(endpoint))
            url_parsed[2] = url_path
            url_parsed[4] = urlencode({'api-version': '3.0-preview'})
            url = urlunparse(url_parsed)
            sesh.put(url)
            current_files_count += 1
            print_progress(0,
                           os.path.normpath(os.path.join(rel_path, '_.dir')))

        if show_progress:
            print('[{}/{}] files, [{}/{}] bytes sent'.format(
                current_files_count,
                total_files_count,
                current_files_size['size'],
                total_files_size), file=sys.stderr)

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

def upgrade(  # pylint: disable=too-many-arguments,too-many-locals
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
    """
    Starts upgrading an application in the Service Fabric cluster.
    Validates the supplied application upgrade parameters and starts upgrading
    the application if the parameters are valid. Please note that upgrade
    description replaces the existing application description. This means that
    if the parameters are not specified, the existing parameters on the
    applications will be overwritten with the empty parameters list. This
    would results in application using the default value of the parameters
    from the application manifest.
    :param str app_id: The identity of the application. This is typically the
    full name of the application without the 'fabric:' URI scheme.
    :param str app_version: The target application type version (found in the
    application manifest) for the application upgrade.
    :param str parameters: A JSON encoded list of application parameter
    overrides to be applied when upgrading the application.
    :param str mode: The mode used to monitor health during a rolling upgrade.
    :param int replica_set_check_timeout: The maximum amount of time to block
    processing of an upgrade domain and prevent loss of availability when
    there are unexpected issues. Measured in seconds.
    :param bool force_restart: Forcefully restart processes during upgrade even
    when the code version has not changed.
    :param str failure_action: The action to perform when a Monitored upgrade
    encounters monitoring policy or health policy violations.
    :param str health_check_wait_duration: The amount of time to wait after
    completing an upgrade domain before applying health policies. Measured in
    milliseconds.
    :param str health_check_stable_duration: The amount of time that the
    application or cluster must remain healthy before the upgrade proceeds
    to the next upgrade domain. Measured in milliseconds.
    :param str health_check_retry_timeout: The amount of time to retry health
    evaluations when the application or cluster is unhealthy before the failure
    action is executed. Measured in milliseconds.
    :param str upgrade_timeout: The amount of time the overall upgrade has to
    complete before FailureAction is executed. Measured in milliseconds.
    :param str upgrade_domain_timeout: The amount of time each upgrade domain
    has to complete before FailureAction is executed. Measured in milliseconds.
    :param bool warning_as_error: Treat health evaluation warnings with the
    same severity as errors.
    :param int max_unhealthy_apps: The maximum allowed percentage of unhealthy
    deployed applications. Represented as a number between 0 and 100.
    :param str default_service_health_policy: JSON encoded specification of the
    health policy used by default to evaluate the health of a service type.
    :param str service_health_policy: JSON encoded map with service type health
    policy per service type name. The map is empty be default.
    """
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
