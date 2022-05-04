# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Custom cluster upgrade specific commands"""

from knack.util import CLIError

def create_monitoring_policy(failure_action, health_check_wait, #pylint: disable=too-many-arguments
                             health_check_stable, health_check_retry,
                             upgrade_timeout, upgrade_domain_timeout):
    """Create a monitoring policy description for an upgrade"""

    if failure_action not in ['Invalid', 'Rollback', 'Manual', None]:
        raise CLIError('Invalid upgrade failure action specified')

    if not any([failure_action, health_check_wait, health_check_stable,
                health_check_retry, upgrade_timeout, upgrade_domain_timeout]):
        return None
    return {
        "FailureAction": failure_action,
        "HealthCheckWaitDurationInMilliseconds": health_check_wait,
        "HealthCheckStableDurationInMilliseconds": health_check_stable,
        "HealthCheckRetryTimeoutInMilliseconds": health_check_retry,
        "UpgradeTimeoutInMilliseconds": upgrade_timeout,
        "UpgradeDomainTimeoutInMilliseconds": upgrade_domain_timeout
        }

def create_upgrade_health_policy(delta_unhealthy_nodes,
                                 ud_delta_unhealthy_nodes):
    """Create an upgrade node health policy"""

    if not any([delta_unhealthy_nodes, ud_delta_unhealthy_nodes]):
        return None
    return {
        "MaxPercentDeltaUnhealthyNodes": delta_unhealthy_nodes,
        "MaxPercentUpgradeDomainDeltaUnhealthyNodes":ud_delta_unhealthy_nodes
    }

def create_cluster_health_policy(warning_as_error, unhealthy_nodes,
                                 unhealthy_applications,
                                 application_type_health_map):
    """Create a cluster health policy for an upgrade"""

    app_type_list = None
    if application_type_health_map:
        app_type_list = []
        for app_type in application_type_health_map:
            allowed_unhealthy = application_type_health_map[app_type]
            policy_item = {"Key": app_type,
                           "Value": allowed_unhealthy}
            app_type_list.append(policy_item)

    if not any([warning_as_error, unhealthy_nodes, unhealthy_applications,
                app_type_list]):
        return None
    return {"ConsiderWarningAsError": warning_as_error,
            "MaxPercentUnhealthyNodes": unhealthy_nodes,
            "MaxPercentUnhealthyApplications": unhealthy_applications,
            "ApplicationTypeHealthPolicyMap": app_type_list}

def parse_app_health_policy(app_health_map):
    """From a complex object create a map of application health policies"""

    if not app_health_map:
        return None
    policy_list = []
    for app in app_health_map:
        allowed_unhealthy = app_health_map[app]
        policy_item = {"Key":app, "Value":allowed_unhealthy} 
        policy_list.append(policy_item)

    return { "ApplicationHealthPolicyMap":policy_list}

def create_rolling_update_desc( #pylint: disable=too-many-arguments
        rolling_upgrade_mode, force_restart, replica_set_check_timeout,
        failure_action, health_check_wait, health_check_stable,
        health_check_retry, upgrade_timeout, upgrade_domain_timeout):
    """Create an update description for an upgrade rolling mode"""

    return {
        "RollingUpgradeMode": rolling_upgrade_mode,
        "ForceRestart": force_restart,
        "ReplicaSetCheckTimeoutInMilliseconds": replica_set_check_timeout, #pylint: disable=line-too-long
        "FailureAction":failure_action,
        "HealthCheckWaitDurationInMilliseconds": health_check_wait,
        "HealthCheckStableDurationInMilliseconds":health_check_stable,
        "HealthCheckRetryTimeoutInMilliseconds": health_check_retry,
        "UpgradeDomainTimeoutInMilliseconds": upgrade_domain_timeout,
        "UpgradeTimeoutInMilliseconds": upgrade_timeout}

def upgrade( #pylint: disable=too-many-locals,missing-docstring,invalid-name,too-many-arguments
        client, code_version=None, config_version=None,
        rolling_upgrade_mode='UnmonitoredAuto', replica_set_check_timeout=None,
        force_restart=False, failure_action=None, health_check_wait=None,
        health_check_stable=None, health_check_retry=None,
        upgrade_timeout=None, upgrade_domain_timeout=None,
        warning_as_error=False, unhealthy_nodes=0, unhealthy_applications=0,
        app_type_health_map=None, delta_health_evaluation=False,
        delta_unhealthy_nodes=10, upgrade_domain_delta_unhealthy_nodes=15,
        app_health_map=None, timeout=60):

    mon_policy = create_monitoring_policy(failure_action, health_check_wait,
                                          health_check_stable,
                                          health_check_retry, upgrade_timeout,
                                          upgrade_domain_timeout)
    cluster_policy = create_cluster_health_policy(
        warning_as_error, unhealthy_nodes, unhealthy_applications,
        app_type_health_map
    )
    cluster_upgrade_policy = create_upgrade_health_policy(
        delta_unhealthy_nodes, upgrade_domain_delta_unhealthy_nodes)
    app_health_policy = parse_app_health_policy(app_health_map)

    upgrade_desc = {
        "CodeVersion": code_version, "ConfigVersion": config_version,
        "UpgradeKind": 'Rolling', "RollingUpgradeMode": rolling_upgrade_mode,
        "UpgradeReplicaSetCheckTimeoutInSeconds": replica_set_check_timeout,
        "ForceRestart": force_restart, "MonitoringPolicy": mon_policy,
        "ClusterHealthPolicy": cluster_policy,
        "EnableDeltaHealthEvaluation": delta_health_evaluation,
        "ClusterUpgradeHealthPolicy": cluster_upgrade_policy,
        "ApplicationHealthPolicyMap":app_health_policy}

    client.start_cluster_upgrade(upgrade_desc, timeout=timeout)

def sa_configuration_upgrade( #pylint: disable=missing-docstring,invalid-name,too-many-arguments,too-many-locals
        client, cluster_config, health_check_retry='P0D',
        health_check_wait='P0D', health_check_stable='P0D',
        upgrade_domain_timeout='P0D', upgrade_timeout='P0D',
        unhealthy_applications=0, unhealthy_nodes=0, delta_unhealthy_nodes=0,
        upgrade_domain_delta_unhealthy_nodes=0, application_health_policies=None, timeout=60):

    app_health_policies = parse_app_health_policy(application_health_policies)

    upgrade_desc = {
        "ClusterConfig": cluster_config,
        "HealthCheckRetryTimeout": health_check_retry,
        "HealthCheckWaitDurationInSeconds": health_check_wait,
        "HealthCheckStableDurationInSeconds": health_check_stable,
        "UpgradeDomainTimeoutInSeconds": upgrade_domain_timeout,
        "UpgradeTimeoutInSeconds": upgrade_timeout,
        "MaxPercentUnhealthyApplications": unhealthy_applications,
        "MaxPercentUnhealthyNodes": unhealthy_nodes,
        "MaxPercentDeltaUnhealthyNodes":delta_unhealthy_nodes,
        "MaxPercentUpgradeDomainDeltaUnhealthyNodes": upgrade_domain_delta_unhealthy_nodes, #pylint: disable=line-too-long
        "ApplicationHealthPolicies": app_health_policies}

    client.start_cluster_configuration_upgrade(upgrade_desc, timeout=timeout)

def update_upgrade( #pylint: disable=too-many-locals,missing-docstring,invalid-name,too-many-arguments
        client, upgrade_kind='Rolling', rolling_upgrade_mode='UnmonitoredAuto',
        replica_set_check_timeout=None, force_restart=False,
        failure_action=None, health_check_wait=None, health_check_stable=None,
        health_check_retry=None, upgrade_timeout=None,
        upgrade_domain_timeout=None, warning_as_error=False, unhealthy_nodes=0,
        unhealthy_applications=0, app_type_health_map=None,
        delta_health_evaluation=False, delta_unhealthy_nodes=10,
        upgrade_domain_delta_unhealthy_nodes=15, app_health_map=None,
        timeout=60):

    rolling_desc = create_rolling_update_desc(
        rolling_upgrade_mode, force_restart, replica_set_check_timeout,
        failure_action, health_check_wait, health_check_stable,
        health_check_retry, upgrade_timeout, upgrade_domain_timeout
    )
    health_policy = create_cluster_health_policy(
        warning_as_error, unhealthy_nodes, unhealthy_applications,
        app_type_health_map
    )
    upgrade_health_policy = create_upgrade_health_policy(
        delta_unhealthy_nodes, upgrade_domain_delta_unhealthy_nodes
    )
    app_policies = parse_app_health_policy(app_health_map)

    update_desc = {
        "UpgradeKind":upgrade_kind, "UpdateDescription":rolling_desc,
        "ClusterHealthPolicy": health_policy,
        "EnableDeltaHealthEvaluation": delta_health_evaluation,
        "ClusterUpgradeHealthPolicy": upgrade_health_policy,
        "ApplicationHealthPolicyMap": app_policies
    }

    client.update_cluster_upgrade(update_desc, timeout=timeout)

def provision(client, cluster_manifest_file_path, code_file_path, timeout=60):
    """
    Provision the code or configuration packages of a Service Fabric cluster.
    :param cluster_manifest_file_path: The cluster manifest file path.
    :param code_file_path: The cluster code package file path.

    """
    payload = {
        "ClusterManifestFilePath": cluster_manifest_file_path,
        "CodeFilePath": code_file_path
    }
    client.provision_cluster(payload, timeout=timeout)

def unprovision_cluster(client, code_version, config_version, timeout=60):
    """
    Unprovision the code or configuration packages of a Service Fabric cluster.
    :param code_version:  The cluster code package version.
    :param config_version: The cluster manifest version.
    """
    payload = {
        "CodeVersion": code_version,
        "ConfigVersion": config_version
    }
    client.unprovision_cluster(payload, timeout=timeout)

def resume_cluster_upgrade(client, upgrade_domain, timeout=60):
    """
    Make the cluster upgrade move on to the next upgrade domain.
    :param upgrade_domain: The next upgrade domain for this cluster upgrade.

    """
    payload = {
        "UpgradeDomain": upgrade_domain,
    }
    client.resume_cluster_upgrade(payload, timeout=timeout)