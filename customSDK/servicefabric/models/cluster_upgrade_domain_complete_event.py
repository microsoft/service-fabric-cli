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

from .cluster_event import ClusterEvent


class ClusterUpgradeDomainCompleteEvent(ClusterEvent):
    """Cluster Upgrade Domain Complete event.

    :param event_instance_id: The identifier for the FabricEvent instance.
    :type event_instance_id: str
    :param time_stamp: The time event was logged.
    :type time_stamp: datetime
    :param has_correlated_events: Shows there is existing related events
     available.
    :type has_correlated_events: bool
    :param kind: Constant filled by server.
    :type kind: str
    :param target_cluster_version: Target Cluster version.
    :type target_cluster_version: str
    :param upgrade_state: State of upgrade.
    :type upgrade_state: str
    :param upgrade_domains: Upgrade domains.
    :type upgrade_domains: str
    :param upgrade_domain_elapsed_time_in_ms: Duration of domain upgrade in
     milli-seconds.
    :type upgrade_domain_elapsed_time_in_ms: float
    """

    _validation = {
        'event_instance_id': {'required': True},
        'time_stamp': {'required': True},
        'kind': {'required': True},
        'target_cluster_version': {'required': True},
        'upgrade_state': {'required': True},
        'upgrade_domains': {'required': True},
        'upgrade_domain_elapsed_time_in_ms': {'required': True},
    }

    _attribute_map = {
        'event_instance_id': {'key': 'EventInstanceId', 'type': 'str'},
        'time_stamp': {'key': 'TimeStamp', 'type': 'iso-8601'},
        'has_correlated_events': {'key': 'HasCorrelatedEvents', 'type': 'bool'},
        'kind': {'key': 'Kind', 'type': 'str'},
        'target_cluster_version': {'key': 'TargetClusterVersion', 'type': 'str'},
        'upgrade_state': {'key': 'UpgradeState', 'type': 'str'},
        'upgrade_domains': {'key': 'UpgradeDomains', 'type': 'str'},
        'upgrade_domain_elapsed_time_in_ms': {'key': 'UpgradeDomainElapsedTimeInMs', 'type': 'float'},
    }

    def __init__(self, event_instance_id, time_stamp, target_cluster_version, upgrade_state, upgrade_domains, upgrade_domain_elapsed_time_in_ms, has_correlated_events=None):
        super(ClusterUpgradeDomainCompleteEvent, self).__init__(event_instance_id=event_instance_id, time_stamp=time_stamp, has_correlated_events=has_correlated_events)
        self.target_cluster_version = target_cluster_version
        self.upgrade_state = upgrade_state
        self.upgrade_domains = upgrade_domains
        self.upgrade_domain_elapsed_time_in_ms = upgrade_domain_elapsed_time_in_ms
        self.kind = 'ClusterUpgradeDomainComplete'
