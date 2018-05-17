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
    from azure.servicefabric.models.monitoring_policy_description import MonitoringPolicyDescription

    if failure_action not in ['Invalid', 'Rollback', 'Manual', None]:
        raise CLIError('Invalid upgrade failure action specified')

    if not any([failure_action, health_check_wait, health_check_stable,
                health_check_retry, upgrade_timeout, upgrade_domain_timeout]):
        return None
    return MonitoringPolicyDescription(
        failure_action=failure_action,
        health_check_wait_duration_in_milliseconds=health_check_wait,
        health_check_stable_duration_in_milliseconds=health_check_stable,
        health_check_retry_timeout_in_milliseconds=health_check_retry,
        upgrade_timeout_in_milliseconds=upgrade_timeout,
        upgrade_domain_timeout_in_milliseconds=upgrade_domain_timeout)

def create_upgrade_health_policy(delta_unhealthy_nodes,
                                 ud_delta_unhealthy_nodes):
    """Create an upgrade node health policy"""
    from azure.servicefabric.models.cluster_upgrade_health_policy_object \
        import ClusterUpgradeHealthPolicyObject

    if not any([delta_unhealthy_nodes, ud_delta_unhealthy_nodes]):
        return None
    return ClusterUpgradeHealthPolicyObject(
        max_percent_delta_unhealthy_nodes=delta_unhealthy_nodes,
        max_percent_upgrade_domain_delta_unhealthy_nodes=ud_delta_unhealthy_nodes
    )

def create_cluster_health_policy(warning_as_error, unhealthy_nodes,
                                 unhealthy_applications,
                                 application_type_health_map):
    """Create a cluster health policy for an upgrade"""
    from azure.servicefabric.models.cluster_health_policy import ClusterHealthPolicy
    from azure.servicefabric.models.application_type_health_policy_map_item \
        import ApplicationTypeHealthPolicyMapItem

    app_type_list = None
    if application_type_health_map:
        app_type_list = []
        for app_type in application_type_health_map:
            allowed_unhealthy = application_type_health_map[app_type]
            policy_item = ApplicationTypeHealthPolicyMapItem(key=app_type,
                                                             value=allowed_unhealthy)
            app_type_list.append(policy_item)

    if not any([warning_as_error, unhealthy_nodes, unhealthy_applications,
                app_type_list]):
        return None
    return ClusterHealthPolicy(consider_warning_as_error=warning_as_error,
                               max_percent_unhealthy_nodes=unhealthy_nodes,
                               max_percent_unhealthy_applications=unhealthy_applications,
                               application_type_health_policy_map=app_type_list)

def parse_app_health_policy(app_health_map):
    """From a complex object create a map of application health policies"""
    from azure.servicefabric.models.application_health_policy_map_item \
        import ApplicationHealthPolicyMapItem
    from azure.servicefabric.models.application_health_policies import ApplicationHealthPolicies

    if not app_health_map:
        return None
    policy_list = []
    for app in app_health_map:
        allowed_unhealthy = app_health_map[app]
        policy_item = ApplicationHealthPolicyMapItem(key=app, value=allowed_unhealthy)
        policy_list.append(policy_item)

    return ApplicationHealthPolicies(application_health_policy_map=policy_list)

def create_rolling_update_desc( #pylint: disable=too-many-arguments
        rolling_upgrade_mode, force_restart, replica_set_check_timeout,
        failure_action, health_check_wait, health_check_stable,
        health_check_retry, upgrade_timeout, upgrade_domain_timeout):
    """Create an update description for an upgrade rolling mode"""
    from azure.servicefabric.models.rolling_upgrade_update_description \
        import RollingUpgradeUpdateDescription

    return RollingUpgradeUpdateDescription(
        rolling_upgrade_mode=rolling_upgrade_mode,
        force_restart=force_restart,
        replica_set_check_timeout_in_milliseconds=replica_set_check_timeout, #pylint: disable=line-too-long
        failure_action=failure_action,
        health_check_wait_duration_in_milliseconds=health_check_wait,
        health_check_stable_duration_in_milliseconds=health_check_stable,
        health_check_retry_timeout_in_milliseconds=health_check_retry,
        upgrade_domain_timeout_in_milliseconds=upgrade_domain_timeout,
        upgrade_timeout_in_milliseconds=upgrade_timeout)

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
    from azure.servicefabric.models.start_cluster_upgrade_description \
        import StartClusterUpgradeDescription

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

    upgrade_desc = StartClusterUpgradeDescription(
        code_version=code_version, config_version=config_version,
        upgrade_kind='Rolling', rolling_upgrade_mode=rolling_upgrade_mode,
        upgrade_replica_set_check_timeout_in_seconds=replica_set_check_timeout,
        force_restart=force_restart, monitoring_policy=mon_policy,
        cluster_health_policy=cluster_policy,
        enable_delta_health_evaluation=delta_health_evaluation,
        cluster_upgrade_health_policy=cluster_upgrade_policy,
        application_health_policy_map=app_health_policy)

    client.start_cluster_upgrade(upgrade_desc, timeout=timeout)

def sa_configuration_upgrade( #pylint: disable=missing-docstring,invalid-name,too-many-arguments
        client, cluster_config, health_check_retry='PT0H0M0S',
        health_check_wait='PT0H0M0S', health_check_stable='PT0H0M0S',
        upgrade_domain_timeout='PT0H0M0S', upgrade_timeout='PT0H0M0S',
        unhealthy_applications=0, unhealthy_nodes=0, delta_unhealthy_nodes=0,
        upgrade_domain_delta_unhealthy_nodes=0, timeout=60):
    from azure.servicefabric.models.cluster_configuration_upgrade_description \
        import ClusterConfigurationUpgradeDescription

    upgrade_desc = ClusterConfigurationUpgradeDescription(
        cluster_config=cluster_config, health_check_retry_timeout=health_check_retry,
        health_check_wait_duration_in_seconds=health_check_wait,
        health_check_stable_duration_in_seconds=health_check_stable,
        upgrade_domain_timeout_in_seconds=upgrade_domain_timeout,
        upgrade_timeout_in_seconds=upgrade_timeout,
        max_percent_unhealthy_applications=unhealthy_applications,
        max_percent_unhealthy_nodes=unhealthy_nodes,
        max_percent_delta_unhealthy_nodes=delta_unhealthy_nodes,
        max_percent_upgrade_domain_delta_unhealthy_nodes=upgrade_domain_delta_unhealthy_nodes) #pylint: disable=line-too-long

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
    from azure.servicefabric.models.update_cluster_upgrade_description \
        import UpdateClusterUpgradeDescription

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

    update_desc = UpdateClusterUpgradeDescription(
        upgrade_kind=upgrade_kind, update_description=rolling_desc,
        cluster_health_policy=health_policy,
        enable_delta_health_evaluation=delta_health_evaluation,
        cluster_upgrade_health_policy=upgrade_health_policy,
        application_health_policy_map=app_policies
    )

    client.update_cluster_upgrade(update_desc, timeout=timeout)
