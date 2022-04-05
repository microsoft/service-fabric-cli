# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class ClusterUpgradeDescriptionObject(Model):
    """Represents a ServiceFabric cluster upgrade.

    :param config_version: The cluster configuration version (specified in the
     cluster manifest).
    :type config_version: str
    :param code_version: The ServiceFabric code version of the cluster.
    :type code_version: str
    :param upgrade_kind: The kind of upgrade out of the following possible
     values. Possible values include: 'Invalid', 'Rolling'. Default value:
     "Rolling" .
    :type upgrade_kind: str or ~azure.servicefabric.models.UpgradeKind
    :param rolling_upgrade_mode: The mode used to monitor health during a
     rolling upgrade. The values are UnmonitoredAuto, UnmonitoredManual,
     Monitored, and UnmonitoredDeferred. Possible values include: 'Invalid',
     'UnmonitoredAuto', 'UnmonitoredManual', 'Monitored',
     'UnmonitoredDeferred'. Default value: "UnmonitoredAuto" .
    :type rolling_upgrade_mode: str or ~azure.servicefabric.models.UpgradeMode
    :param upgrade_replica_set_check_timeout_in_seconds: The maximum amount of
     time to block processing of an upgrade domain and prevent loss of
     availability when there are unexpected issues. When this timeout expires,
     processing of the upgrade domain will proceed regardless of availability
     loss issues. The timeout is reset at the start of each upgrade domain.
     Valid values are between 0 and 42949672925 inclusive. (unsigned 32-bit
     integer).
    :type upgrade_replica_set_check_timeout_in_seconds: long
    :param force_restart: If true, then processes are forcefully restarted
     during upgrade even when the code version has not changed (the upgrade
     only changes configuration or data).
    :type force_restart: bool
    :param sort_order: Defines the order in which an upgrade proceeds through
     the cluster. Possible values include: 'Invalid', 'Default', 'Numeric',
     'Lexicographical', 'ReverseNumeric', 'ReverseLexicographical'. Default
     value: "Default" .
    :type sort_order: str or ~azure.servicefabric.models.UpgradeSortOrder
    :param enable_delta_health_evaluation: When true, enables delta health
     evaluation rather than absolute health evaluation after completion of each
     upgrade domain.
    :type enable_delta_health_evaluation: bool
    :param monitoring_policy: Describes the parameters for monitoring an
     upgrade in Monitored mode.
    :type monitoring_policy:
     ~azure.servicefabric.models.MonitoringPolicyDescription
    :param cluster_health_policy: Defines a health policy used to evaluate the
     health of the cluster or of a cluster node.
    :type cluster_health_policy:
     ~azure.servicefabric.models.ClusterHealthPolicy
    :param cluster_upgrade_health_policy: Defines a health policy used to
     evaluate the health of the cluster during a cluster upgrade.
    :type cluster_upgrade_health_policy:
     ~azure.servicefabric.models.ClusterUpgradeHealthPolicyObject
    :param application_health_policy_map: Represents the map of application
     health policies for a ServiceFabric cluster upgrade
    :type application_health_policy_map:
     ~azure.servicefabric.models.ApplicationHealthPolicyMapObject
    """

    _attribute_map = {
        'config_version': {'key': 'ConfigVersion', 'type': 'str'},
        'code_version': {'key': 'CodeVersion', 'type': 'str'},
        'upgrade_kind': {'key': 'UpgradeKind', 'type': 'str'},
        'rolling_upgrade_mode': {'key': 'RollingUpgradeMode', 'type': 'str'},
        'upgrade_replica_set_check_timeout_in_seconds': {'key': 'UpgradeReplicaSetCheckTimeoutInSeconds', 'type': 'long'},
        'force_restart': {'key': 'ForceRestart', 'type': 'bool'},
        'sort_order': {'key': 'SortOrder', 'type': 'str'},
        'enable_delta_health_evaluation': {'key': 'EnableDeltaHealthEvaluation', 'type': 'bool'},
        'monitoring_policy': {'key': 'MonitoringPolicy', 'type': 'MonitoringPolicyDescription'},
        'cluster_health_policy': {'key': 'ClusterHealthPolicy', 'type': 'ClusterHealthPolicy'},
        'cluster_upgrade_health_policy': {'key': 'ClusterUpgradeHealthPolicy', 'type': 'ClusterUpgradeHealthPolicyObject'},
        'application_health_policy_map': {'key': 'ApplicationHealthPolicyMap', 'type': 'ApplicationHealthPolicyMapObject'},
    }

    def __init__(self, **kwargs):
        super(ClusterUpgradeDescriptionObject, self).__init__(**kwargs)
        self.config_version = kwargs.get('config_version', None)
        self.code_version = kwargs.get('code_version', None)
        self.upgrade_kind = kwargs.get('upgrade_kind', "Rolling")
        self.rolling_upgrade_mode = kwargs.get('rolling_upgrade_mode', "UnmonitoredAuto")
        self.upgrade_replica_set_check_timeout_in_seconds = kwargs.get('upgrade_replica_set_check_timeout_in_seconds', None)
        self.force_restart = kwargs.get('force_restart', None)
        self.sort_order = kwargs.get('sort_order', "Default")
        self.enable_delta_health_evaluation = kwargs.get('enable_delta_health_evaluation', None)
        self.monitoring_policy = kwargs.get('monitoring_policy', None)
        self.cluster_health_policy = kwargs.get('cluster_health_policy', None)
        self.cluster_upgrade_health_policy = kwargs.get('cluster_upgrade_health_policy', None)
        self.application_health_policy_map = kwargs.get('application_health_policy_map', None)
