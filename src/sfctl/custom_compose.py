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

def repo_creds(username, password, encrypted):
    """Get a representation of the container repository credentials"""
    from azure.servicefabric.models import RegistryCredential

    if encrypted and not all([username, password]):
        raise CLIError('Cannot specify empty encrypted credentials')
    if password and not username:
        raise CLIError('Missing username')
    if not any([username, password, encrypted]):
        return None

    return RegistryCredential(registry_user_name=username,
                              registry_password=password,
                              password_encrypted=encrypted)

def create_app_health_policy(
    warning_as_error, unhealthy_app, default_svc_health_map,
    svc_type_health_map):
    from sfctl.custom_health import (parse_service_health_policy,
                                     parse_service_health_policy_map)
    from azure.servicefabric.models import ApplicationHealthPolicy

    default_svc_type_policy = parse_service_health_policy(
        default_svc_health_map
    )
    svc_type_policy = parse_service_health_policy_map(svc_type_health_map)

    return ApplicationHealthPolicy(
        consider_warning_as_error=warning_as_error,
        max_percent_unhealthy_deployed_applications=unhealthy_app,
        default_service_type_health_policy=default_svc_type_policy,
        service_type_health_policy_map=svc_type_policy
    )

def upgrade(client, name, file_path, user=None, has_pass=False, #pylint: disable=missing-docstring,too-many-locals
            encrypted_pass=None, upgrade_kind='Rolling',
            upgrade_mode='UnmonitoredAuto', replica_set_check=None,
            force_restart=False, failure_action=None, health_check_wait=None,
            health_check_stable=None, health_check_retry=None,
            upgrade_timeout=None, upgrade_domain_timeout=None,
            warning_as_error=False, unhealthy_app=0,
            default_svc_type_health_map=None, svc_type_health_map=None,
            timeout=60):
    from azure.servicefabric.models import ComposeDeploymentUpgradeDescription
    from getpass import getpass
    from sfctl.custom_cluster_upgrade import create_monitoring_policy

    file_contents = read_file(file_path)

    pass_phrase = None
    if has_pass and not encrypted_pass:
        pass_phrase = getpass('Container repository password: ')
    elif encrypted_pass is not None:
        pass_phrase = encrypted_pass
    encrypted = True if encrypted_pass is not None else False
    credentials = repo_creds(user, pass_phrase, encrypted)

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

    desc = ComposeDeploymentUpgradeDescription(
        name, file_contents, registry_credential=credentials,
        upgrade_kind=upgrade_kind, rolling_upgrade_mode=upgrade_mode,
        upgrade_replica_set_check_timeout_in_seconds=replica_set_check,
        force_restart=force_restart, monitoring_policy=monitoring_policy,
        application_health_policy=app_health_policy)

    client.start_compose_deployment_upgrade(name, desc, timeout=timeout)
