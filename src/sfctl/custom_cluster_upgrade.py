# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Custom cluster upgrade specific commands"""

from knack.util import CLIError

def create_monitoring_policy(failure_action, health_check_wait,
                             health_check_stable, health_check_retry,
                             upgrade_timeout, upgrade_domain_timeout):
    """Create a monitoring policy description for an upgrade"""
    from azure.servicefabric.models import MonitoringPolicyDescription

    if failure_action not in ['Invalid', 'Rollback', 'Manual', None]:
        raise CLIError('Invalid upgrade failure action specified')

    if not any([failure_action, health_check_wait, health_check_stable,
                health_check_retry, upgrade_timeout, upgrade_domain_timeout]):
        return None
    return MonitoringPolicyDescription(failure_action, health_check_wait,
                                       health_check_stable, health_check_retry,
                                       upgrade_timeout, upgrade_domain_timeout)

def create_upgrade_health_policy(delta_unhealthy_nodes,
                                 ud_delta_unhealthy_nodes):
    """Create an upgrade node health policy"""
    from azure.servicefabric.models import ClusterUpgradeHealthPolicyObject

    if not any([delta_unhealthy_nodes, ud_delta_unhealthy_nodes]):
        return None
    return ClusterUpgradeHealthPolicyObject(
        delta_unhealthy_nodes, ud_delta_unhealthy_nodes
    )

def create_cluster_health_policy(warning_as_error, unhealthy_nodes,
                                 unhealthy_applications,
                                 application_type_health_map):
    """Create a cluster health policy for an upgrade"""
    from azure.servicefabric.models import (ClusterHealthPolicy,
                                            ApplicationTypeHealthPolicyMapItem)

    app_type_list = None
    if application_type_health_map:
        app_type_list = []
        for app_type in application_type_health_map:
            allowed_unhealthy = application_type_health_map[app_type]
            policy_item = ApplicationTypeHealthPolicyMapItem(app_type,
                                                             allowed_unhealthy)
            app_type_list.append(policy_item)

    if not any([warning_as_error, unhealthy_nodes, unhealthy_applications,
                app_type_list]):
        return None
    return ClusterHealthPolicy(warning_as_error, unhealthy_nodes,
                               unhealthy_applications, app_type_list)

def parse_app_health_policy(app_health_map):
    """From a complex object create a map of application health policies"""
    from azure.servicefabric.models import (ApplicationHealthPolicyMapItem,
                                            ApplicationHealthPolicies)
    if not app_health_map:
        return None
    policy_list = []
    for app in app_health_map:
        allowed_unhealthy = app_health_map[app]
        policy_item = ApplicationHealthPolicyMapItem(app, allowed_unhealthy)
        policy_list.append(policy_item)

    return ApplicationHealthPolicies(policy_list)

def upgrade( #pylint: disable=too-many-locals,missing-docstring,invalid-name
        client, code_version=None, config_version=None,
        rolling_upgrade_mode='UnmonitoredAuto', replica_set_check_timeout=None,
        force_restart=False, failure_action=None, health_check_wait=None,
        health_check_stable=None, health_check_retry=None,
        upgrade_timeout=None, upgrade_domain_timeout=None,
        warning_as_error=False, unhealthy_nodes=0, unhealthy_applications=0,
        app_type_health_map=None, delta_health_evaluation=False,
        delta_unhealthy_nodes=10, upgrade_domain_delta_unhealthy_nodes=15,
        app_health_map=None, timeout=60):
    from azure.servicefabric.models import StartClusterUpgradeDescription

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