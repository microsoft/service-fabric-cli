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

from .cluster_event_py3 import ClusterEvent


class ClusterUpgradeRollbackStartedEvent(ClusterEvent):
    """Cluster Upgrade Rollback Started event.

    All required parameters must be populated in order to send to Azure.

    :param event_instance_id: Required. The identifier for the FabricEvent
     instance.
    :type event_instance_id: str
    :param category: The category of event.
    :type category: str
    :param time_stamp: Required. The time event was logged.
    :type time_stamp: datetime
    :param has_correlated_events: Shows there is existing related events
     available.
    :type has_correlated_events: bool
    :param kind: Required. Constant filled by server.
    :type kind: str
    :param target_cluster_version: Required. Target Cluster version.
    :type target_cluster_version: str
    :param failure_reason: Required. Describes failure.
    :type failure_reason: str
    :param overall_upgrade_elapsed_time_in_ms: Required. Overall duration of
     upgrade in milli-seconds.
    :type overall_upgrade_elapsed_time_in_ms: float
    """

    _validation = {
        'event_instance_id': {'required': True},
        'time_stamp': {'required': True},
        'kind': {'required': True},
        'target_cluster_version': {'required': True},
        'failure_reason': {'required': True},
        'overall_upgrade_elapsed_time_in_ms': {'required': True},
    }

    _attribute_map = {
        'event_instance_id': {'key': 'EventInstanceId', 'type': 'str'},
        'category': {'key': 'Category', 'type': 'str'},
        'time_stamp': {'key': 'TimeStamp', 'type': 'iso-8601'},
        'has_correlated_events': {'key': 'HasCorrelatedEvents', 'type': 'bool'},
        'kind': {'key': 'Kind', 'type': 'str'},
        'target_cluster_version': {'key': 'TargetClusterVersion', 'type': 'str'},
        'failure_reason': {'key': 'FailureReason', 'type': 'str'},
        'overall_upgrade_elapsed_time_in_ms': {'key': 'OverallUpgradeElapsedTimeInMs', 'type': 'float'},
    }

    def __init__(self, *, event_instance_id: str, time_stamp, target_cluster_version: str, failure_reason: str, overall_upgrade_elapsed_time_in_ms: float, category: str=None, has_correlated_events: bool=None, **kwargs) -> None:
        super(ClusterUpgradeRollbackStartedEvent, self).__init__(event_instance_id=event_instance_id, category=category, time_stamp=time_stamp, has_correlated_events=has_correlated_events, **kwargs)
        self.target_cluster_version = target_cluster_version
        self.failure_reason = failure_reason
        self.overall_upgrade_elapsed_time_in_ms = overall_upgrade_elapsed_time_in_ms
        self.kind = 'ClusterUpgradeRollbackStarted'
