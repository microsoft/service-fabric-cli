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
    from azure.servicefabric.models.registry_credential import RegistryCredential
    from getpass import getpass

    # Wonky since we allow empty string as an encrypted passphrase
    if not any([username, encrypted_password is not None, has_pass]):
        return None

    if (encrypted_password is not None) and (not username):
        raise CLIError('Missing container repository username')

    if has_pass and (not username):
        raise CLIError('Missing container repository username')

    if encrypted_password is not None:
        return RegistryCredential(registry_user_name=username,
                                  registry_password=encrypted_password,
                                  password_encrypted=True)
    elif has_pass:
        passphrase = getpass(prompt='Container repository password: ')
        return RegistryCredential(registry_user_name=username,
                                  registry_password=passphrase,
                                  password_encrypted=False)
    return RegistryCredential(registry_user_name=username)

def create_app_health_policy(
        warning_as_error, unhealthy_app, default_svc_health_map,
        svc_type_health_map):
    """Create an application health policy description"""
    from sfctl.custom_health import (parse_service_health_policy,
                                     parse_service_health_policy_map)
    from azure.servicefabric.models.application_health_policy import ApplicationHealthPolicy

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


def create(client, deployment_name, file_path, user=None, has_pass=False, #pylint: disable=missing-docstring,too-many-arguments
           encrypted_pass=None, timeout=60):
    from azure.servicefabric.models.create_compose_deployment_description \
        import CreateComposeDeploymentDescription

    file_contents = read_file(file_path)
    credentials = repo_creds(user, encrypted_pass, has_pass)
    desc = CreateComposeDeploymentDescription(deployment_name=deployment_name,
                                              compose_file_content=file_contents,
                                              registry_credential=credentials)
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
    from azure.servicefabric.models.compose_deployment_upgrade_description \
        import ComposeDeploymentUpgradeDescription
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

    desc = ComposeDeploymentUpgradeDescription(
        deployment_name=deployment_name,
        compose_file_content=file_contents,
        registry_credential=credentials,
        upgrade_kind=upgrade_kind,
        rolling_upgrade_mode=upgrade_mode,
        upgrade_replica_set_check_timeout_in_seconds=replica_set_check,
        force_restart=force_restart,
        monitoring_policy=monitoring_policy,
        application_health_policy=app_health_policy)

    client.start_compose_deployment_upgrade(deployment_name,
                                            desc,
                                            timeout=timeout)
