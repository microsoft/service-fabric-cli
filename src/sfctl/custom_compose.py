# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Custom commands for the Service Fabric Docker compose support"""

from knack.cli import CLIError

def read_file(file_path):
    """Reads a file contents given a file path"""
    file_contents = None
    with open(file_path) as f_desc:
        file_contents = f_desc.read()
    if not file_contents:
        raise CLIError('Could not read {}'.format(file_path))
    return file_contents

def repo_creds(username, encrypted_password, has_pass):
    """Get a representation of the container repository credentials"""
    from getpass import getpass

    # Wonky since we allow empty string as an encrypted passphrase
    if not any([username, encrypted_password is not None, has_pass]):
        return None

    if (encrypted_password is not None) and (not username):
        raise CLIError('Missing container repository username')

    if has_pass and (not username):
        raise CLIError('Missing container repository username')

    if encrypted_password is not None:
        return { "RegistryUserName": username,
                 "RegistryPassword": encrypted_password,
                 "PasswordEncrypted":True
                 }
    if has_pass:
        passphrase = getpass(prompt='Container repository password: ')
        return {"RegistryUserName": username,
                "RegistryPassword": passphrase,
                "PasswordEncrypted": False
                }

    return { "RegistryUserName": username }

def create_app_health_policy(
        warning_as_error, unhealthy_app, default_svc_health_map,
        svc_type_health_map):
    """Create an application health policy description"""
    from sfctl.custom_health import (parse_service_health_policy,
                                     parse_service_health_policy_map)

    default_svc_type_policy = parse_service_health_policy(
        default_svc_health_map
    )
    svc_type_policy = parse_service_health_policy_map(svc_type_health_map)

    return {
        "ConsiderWarningAsError": warning_as_error,
        "MaxPercentUnhealthyDeployedApplications": unhealthy_app,
        "DefaultServiceTypeHealthPolicy": default_svc_type_policy,
        "ServiceTypeHealthPolicyMap": svc_type_policy
    }


def create(client, deployment_name, file_path, user=None, has_pass=False, #pylint: disable=missing-docstring,too-many-arguments
           encrypted_pass=None, timeout=60):

    file_contents = read_file(file_path)
    credentials = repo_creds(user, encrypted_pass, has_pass)
    desc = {"DeploymentName": deployment_name,
            "ComposeFileContent": file_contents,
            "RegistryCredential": credentials
            }
    client.create_compose_deployment(desc, timeout=timeout)


def upgrade(client, deployment_name, file_path, user=None, has_pass=False, #pylint: disable=missing-docstring,too-many-locals,too-many-arguments
            encrypted_pass=None, upgrade_kind='Rolling',
            upgrade_mode='UnmonitoredAuto', replica_set_check=None,
            force_restart=False, failure_action=None, health_check_wait=None,
            health_check_stable=None, health_check_retry=None,
            upgrade_timeout=None, upgrade_domain_timeout=None,
            warning_as_error=False, unhealthy_app=0,
            default_svc_type_health_map=None, svc_type_health_map=None,
            timeout=60):

    from sfctl.custom_cluster_upgrade import create_monitoring_policy

    file_contents = read_file(file_path)

    credentials = repo_creds(user, encrypted_pass, has_pass)

    monitoring_policy = create_monitoring_policy(failure_action,
                                                 health_check_wait,
                                                 health_check_stable,
                                                 health_check_retry,
                                                 upgrade_timeout,
                                                 upgrade_domain_timeout)

    app_health_policy = create_app_health_policy(warning_as_error,
                                                 unhealthy_app,
                                                 default_svc_type_health_map,
                                                 svc_type_health_map)

    desc = {
        "DeploymentName": deployment_name,
        "ComposeFileContent": file_contents,
        "RegistryCredential": credentials,
        "UpgradeKind": upgrade_kind,
        "RollingUpgradeMode": upgrade_mode,
        "UpgradeReplicaSetCheckTimeoutInSeconds": replica_set_check,
        "ForceRestart": force_restart,
        "MonitoringPolicy": monitoring_policy,
        "ApplicationHealthPolicy": app_health_policy
    }

    client.start_compose_deployment_upgrade(deployment_name,
                                            desc,
                                            timeout=timeout)


def get_compose_deployment_status_list(client, continuation_token=None, max_results=0, timeout=60):
    """Gets the list of compose deployments created in the Service Fabric cluster.

    Gets the status about the compose deployments that were created or in the process of being
    created in the Service Fabric cluster. The response includes the name, status, and other
    details about the compose deployments. If the list of deployments do not fit in a page, one
    page of results is returned as well as a continuation token, which can be used to get the next
    page.

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
    :paramtype max_results: long
    """

    return client.get_compose_deployment_status_list(continuation_token_parameter=continuation_token,
                                                     max_results=max_results, timeout=timeout)
