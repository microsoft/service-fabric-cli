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


class ChaosStartedEvent(ClusterEvent):
    """Chaos Started event.

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
    :param max_concurrent_faults: Required. Maximum number of concurrent
     faults.
    :type max_concurrent_faults: long
    :param time_to_run_in_seconds: Required. Time to run in seconds.
    :type time_to_run_in_seconds: float
    :param max_cluster_stabilization_timeout_in_seconds: Required. Maximum
     timeout for cluster stabilization in seconds.
    :type max_cluster_stabilization_timeout_in_seconds: float
    :param wait_time_between_iterations_in_seconds: Required. Wait time
     between iterations in seconds.
    :type wait_time_between_iterations_in_seconds: float
    :param wait_time_between_faults_in_seconds: Required. Wait time between
     faults in seconds.
    :type wait_time_between_faults_in_seconds: float
    :param move_replica_fault_enabled: Required. Indicates MoveReplica fault
     is enabled.
    :type move_replica_fault_enabled: bool
    :param included_node_type_list: Required. List of included Node types.
    :type included_node_type_list: str
    :param included_application_list: Required. List of included Applications.
    :type included_application_list: str
    :param cluster_health_policy: Required. Health policy.
    :type cluster_health_policy: str
    :param chaos_context: Required. Chaos Context.
    :type chaos_context: str
    """

    _validation = {
        'event_instance_id': {'required': True},
        'time_stamp': {'required': True},
        'kind': {'required': True},
        'max_concurrent_faults': {'required': True},
        'time_to_run_in_seconds': {'required': True},
        'max_cluster_stabilization_timeout_in_seconds': {'required': True},
        'wait_time_between_iterations_in_seconds': {'required': True},
        'wait_time_between_faults_in_seconds': {'required': True},
        'move_replica_fault_enabled': {'required': True},
        'included_node_type_list': {'required': True},
        'included_application_list': {'required': True},
        'cluster_health_policy': {'required': True},
        'chaos_context': {'required': True},
    }

    _attribute_map = {
        'event_instance_id': {'key': 'EventInstanceId', 'type': 'str'},
        'category': {'key': 'Category', 'type': 'str'},
        'time_stamp': {'key': 'TimeStamp', 'type': 'iso-8601'},
        'has_correlated_events': {'key': 'HasCorrelatedEvents', 'type': 'bool'},
        'kind': {'key': 'Kind', 'type': 'str'},
        'max_concurrent_faults': {'key': 'MaxConcurrentFaults', 'type': 'long'},
        'time_to_run_in_seconds': {'key': 'TimeToRunInSeconds', 'type': 'float'},
        'max_cluster_stabilization_timeout_in_seconds': {'key': 'MaxClusterStabilizationTimeoutInSeconds', 'type': 'float'},
        'wait_time_between_iterations_in_seconds': {'key': 'WaitTimeBetweenIterationsInSeconds', 'type': 'float'},
        'wait_time_between_faults_in_seconds': {'key': 'WaitTimeBetweenFaultsInSeconds', 'type': 'float'},
        'move_replica_fault_enabled': {'key': 'MoveReplicaFaultEnabled', 'type': 'bool'},
        'included_node_type_list': {'key': 'IncludedNodeTypeList', 'type': 'str'},
        'included_application_list': {'key': 'IncludedApplicationList', 'type': 'str'},
        'cluster_health_policy': {'key': 'ClusterHealthPolicy', 'type': 'str'},
        'chaos_context': {'key': 'ChaosContext', 'type': 'str'},
    }

    def __init__(self, *, event_instance_id: str, time_stamp, max_concurrent_faults: int, time_to_run_in_seconds: float, max_cluster_stabilization_timeout_in_seconds: float, wait_time_between_iterations_in_seconds: float, wait_time_between_faults_in_seconds: float, move_replica_fault_enabled: bool, included_node_type_list: str, included_application_list: str, cluster_health_policy: str, chaos_context: str, category: str=None, has_correlated_events: bool=None, **kwargs) -> None:
        super(ChaosStartedEvent, self).__init__(event_instance_id=event_instance_id, category=category, time_stamp=time_stamp, has_correlated_events=has_correlated_events, **kwargs)
        self.max_concurrent_faults = max_concurrent_faults
        self.time_to_run_in_seconds = time_to_run_in_seconds
        self.max_cluster_stabilization_timeout_in_seconds = max_cluster_stabilization_timeout_in_seconds
        self.wait_time_between_iterations_in_seconds = wait_time_between_iterations_in_seconds
        self.wait_time_between_faults_in_seconds = wait_time_between_faults_in_seconds
        self.move_replica_fault_enabled = move_replica_fault_enabled
        self.included_node_type_list = included_node_type_list
        self.included_application_list = included_application_list
        self.cluster_health_policy = cluster_health_policy
        self.chaos_context = chaos_context
        self.kind = 'ChaosStarted'
