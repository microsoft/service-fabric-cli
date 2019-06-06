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

from .replica_event import ReplicaEvent


class ChaosReplicaRemovalScheduledEvent(ReplicaEvent):
    """Chaos Remove Replica Fault Scheduled event.

    :param event_instance_id: The identifier for the FabricEvent instance.
    :type event_instance_id: str
    :param category: The category of event.
    :type category: str
    :param time_stamp: The time event was logged.
    :type time_stamp: datetime
    :param has_correlated_events: Shows there is existing related events
     available.
    :type has_correlated_events: bool
    :param kind: Constant filled by server.
    :type kind: str
    :param partition_id: An internal ID used by Service Fabric to uniquely
     identify a partition. This is a randomly generated GUID when the service
     was created. The partition ID is unique and does not change for the
     lifetime of the service. If the same service was deleted and recreated the
     IDs of its partitions would be different.
    :type partition_id: str
    :param replica_id: Id of a stateful service replica. ReplicaId is used by
     Service Fabric to uniquely identify a replica of a partition. It is unique
     within a partition and does not change for the lifetime of the replica. If
     a replica gets dropped and another replica gets created on the same node
     for the same partition, it will get a different value for the id.
     Sometimes the id of a stateless service instance is also referred as a
     replica id.
    :type replica_id: long
    :param fault_group_id: Id of fault group.
    :type fault_group_id: str
    :param fault_id: Id of fault.
    :type fault_id: str
    :param service_uri: Service name.
    :type service_uri: str
    """

    _validation = {
        'event_instance_id': {'required': True},
        'time_stamp': {'required': True},
        'kind': {'required': True},
        'partition_id': {'required': True},
        'replica_id': {'required': True},
        'fault_group_id': {'required': True},
        'fault_id': {'required': True},
        'service_uri': {'required': True},
    }

    _attribute_map = {
        'event_instance_id': {'key': 'EventInstanceId', 'type': 'str'},
        'category': {'key': 'Category', 'type': 'str'},
        'time_stamp': {'key': 'TimeStamp', 'type': 'iso-8601'},
        'has_correlated_events': {'key': 'HasCorrelatedEvents', 'type': 'bool'},
        'kind': {'key': 'Kind', 'type': 'str'},
        'partition_id': {'key': 'PartitionId', 'type': 'str'},
        'replica_id': {'key': 'ReplicaId', 'type': 'long'},
        'fault_group_id': {'key': 'FaultGroupId', 'type': 'str'},
        'fault_id': {'key': 'FaultId', 'type': 'str'},
        'service_uri': {'key': 'ServiceUri', 'type': 'str'},
    }

    def __init__(self, event_instance_id, time_stamp, partition_id, replica_id, fault_group_id, fault_id, service_uri, category=None, has_correlated_events=None):
        super(ChaosReplicaRemovalScheduledEvent, self).__init__(event_instance_id=event_instance_id, category=category, time_stamp=time_stamp, has_correlated_events=has_correlated_events, partition_id=partition_id, replica_id=replica_id)
        self.fault_group_id = fault_group_id
        self.fault_id = fault_id
        self.service_uri = service_uri
        self.kind = 'ChaosReplicaRemovalScheduled'
