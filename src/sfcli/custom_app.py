"""Custom application related CLI commands."""

import os
import sys

from urllib.parse import urlparse, urlunparse, urlencode
from knack.util import CLIError

import requests

def create_compose_application(client, compose_file, application_id,
                               repo_user=None, encrypted=False,
                               repo_pass=None, timeout=60):
    from azure.servicefabric.models.create_compose_application_description import CreateComposeApplicationDescription #pylint: disable=line-too-long
    from azure.servicefabric.models.repository_credential import (
        RepositoryCredential
    )
    from getpass import getpass

    usage = ('Invalid arguments: [ --application_id --compose_file | '
             '--application_id --compose_file --repo_user | '
             '--application_id --compose_file --repo_user --encrypted '
             '--repo_pass ])')

    if (any([encrypted, repo_pass]) and
            not all([encrypted, repo_pass, repo_user])):
        raise CLIError(usage)

    if not encrypted and repo_user:
        repo_pass = getpass('Container repository password: ')

    repo_cred = RepositoryCredential(repo_user, repo_pass, encrypted)

    if not os.path.isfile(compose_file):
        raise CLIError('Cannot find specified Compose file')
    file_contents = None
    with open(compose_file) as c_file:
        file_contents = c_file.read()

    if not file_contents:
        raise CLIError('Could not read Compose file contents')

    model = CreateComposeApplicationDescription(application_id, file_contents,
                                                repo_cred)

    client.create_compose_application(model, timeout)

def validate_app_path(app_path):
    """Validates an application package path and returns the absolute path."""

    abspath = os.path.abspath(app_path)
    if os.path.isdir(abspath):
        return abspath
    else:
        raise ValueError('Invalid path to application '
                         'directory: {0}'.format(abspath))


def sf_upload_app(path, show_progress=False):  # pylint: disable=too-many-locals
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
    from sfcli.config import (client_endpoint, cert_info, ca_cert_info,
                              no_verify_setting)

    abspath = validate_app_path(path)
    basename = os.path.basename(abspath)

    endpoint = client_endpoint()
    cert = cert_info()
    ca_cert = False
    if not no_verify_setting():
        ca_cert = ca_cert_info()
    total_files_count = 0
    current_files_count = 0
    total_files_size = 0
    current_files_size = 0

    for root, _, files in os.walk(abspath):
        total_files_count += (len(files) + 1)
        for cur_file in files:
            stat_info = os.stat(os.path.join(root, cur_file))
            total_files_size += stat_info.st_size

    def print_progress(size, rel_file_path):
        """Display progress for file upload"""
        nonlocal current_files_size
        current_files_size += size
        if show_progress:
            print(
                '[{}/{}] files, [{}/{}] bytes, {}'.format(
                    current_files_count,
                    total_files_count,
                    current_files_size,
                    total_files_size,
                    rel_file_path), file=sys.stderr)

    for root, _, files in os.walk(abspath):
        rel_path = os.path.normpath(os.path.relpath(root, abspath))
        for i in files:
            url_path = (
                os.path.normpath(os.path.join('ImageStore', basename,
                                              rel_path, i))
            ).replace('\\', '/')
            i_file = os.path.normpath(os.path.join(root, i))
            with open(i_file, 'rb') as file_opened:
                url_parsed = list(urlparse(endpoint))
                url_parsed[2] = url_path
                url_parsed[4] = urlencode(
                    {'api-version': '3.0-preview'})
                url = urlunparse(url_parsed)

                def file_chunk(target_file, rel_path, print_progress):
                    """Yield a chunk of file upload and print progress"""
                    chunk = True
                    while chunk:
                        chunk = target_file.read(100000)
                        print_progress(len(chunk), rel_path)
                        yield chunk

                chunk_iter = file_chunk(file_opened, os.path.normpath(
                    os.path.join(rel_path, i)
                ), print_progress)
                requests.put(url, data=chunk_iter, cert=cert,
                             verify=ca_cert)
                current_files_count += 1
                print_progress(0, os.path.normpath(
                    os.path.join(rel_path, i)
                ))
        url_path = (
            os.path.normpath(os.path.join('ImageStore', basename,
                                          rel_path, '_.dir'))
        ).replace('\\', '/')
        url_parsed = list(urlparse(endpoint))
        url_parsed[2] = url_path
        url_parsed[4] = urlencode({'api-version': '3.0-preview'})
        url = urlunparse(url_parsed)
        requests.put(url, cert=cert, verify=ca_cert)
        current_files_count += 1
        print_progress(0, os.path.normpath(os.path.join(rel_path, '_.dir')))

    if show_progress:
        print('[{}/{}] files, [{}/{}] bytes sent'.format(
            current_files_count,
            total_files_count,
            current_files_size,
            total_files_size), file=sys.stderr)


def parse_app_params(formatted_params):
    """Convert a string into a list of application parameters"""

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
    """Convert a string into a list of application metrics."""

    from azure.servicefabric.models.application_metric_description import (
        ApplicationMetricDescription
    )

    if formatted_metrics is None:
        return None

    res = []
    for metric in formatted_metrics:
        metric_name = metric.get("name", None)
        if not metric_name:
            raise CLIError("Could not find required application metric name")

        metric_max_cap = metric.get("maximum_capacity", None)
        metric_reserve_cap = metric.get("reservation_capacity", None)
        metric_total_cap = metric.get("total_application_capacity", None)
        metric_desc = ApplicationMetricDescription(metric_name, metric_max_cap,
                                                   metric_reserve_cap,
                                                   metric_total_cap)
        res.append(metric_desc)
    return res


def sf_create_app(client,  # pylint: disable=too-many-locals,too-many-arguments
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
        raise CLIError("Must specify both maximum and minimum node count")

    if (all([min_node_count, max_node_count]) and
            min_node_count > max_node_count):
        raise CLIError("The minimum node reserve capacity count cannot "
                       "be greater than the maximum node count")

    app_params = parse_app_params(parameters)

    app_metrics = parse_app_metrics(metrics)

    app_cap_desc = ApplicationCapacityDescription(min_node_count,
                                                  max_node_count,
                                                  app_metrics)

    app_desc = ApplicationDescription(app_name, app_type, app_version,
                                      app_params, app_cap_desc)

    client.create_application(app_desc, timeout)

def sf_upgrade_app(  # pylint: disable=too-many-arguments,too-many-locals
        client, app_id, app_version, parameters, mode="UnmonitoredAuto",
        replica_set_check_timeout=None, force_restart=None,
        failure_action=None, health_check_wait_duration="0",
        upgade_timeout="P10675199DT02H48M05.4775807S",
        service_health_policy=None, timeout=60):
    """

    Validates the supplied application upgrade parameters and starts upgrading
    the application if the parameters are valid. Please note that upgrade
    description replaces the existing application description. This means that
    if the parameters are not specified, the existing parameters on the
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
    evaluations whn the application or cluster is unhealthy before the failure
    complete before FailureAction is executed. Measured in milliseconds.

    has to complete before FailureAction is executed. Measured in milliseconds.

    :param bool warning_as_error: Treat health evaluation warnings with the
    same severity as errors.

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

    monitoring_policy = MonitoringPolicyDescription(
        failure_action, health_check_wait_duration,
 )
    if app_params is None:
        app_params = []
    def_shp = parse_default_service_health_policy(default_service_health_policy)

    map_shp = parse_service_health_policy_map(service_health_policy)

    app_health_policy = ApplicationHealthPolicy(warning_as_error,
                                         "Rolling", mode,
                                         replica_set_check_timeout,
                                         force_restart, monitoring_policy,
                                         app_health_policy)

    client.start_application_upgrade(app_id, desc, timeout)
    # TODO consider additional parameter validation here rather than allowing
    # the gateway to reject it and return failure response

