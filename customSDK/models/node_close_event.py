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

from .node_event import NodeEvent


class NodeCloseEvent(NodeEvent):
    """Node Close event.

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
    :param node_name: The name of a Service Fabric node.
    :type node_name: str
    :param node_id: Id of Node.
    :type node_id: str
    :param node_instance: Id of Node instance.
    :type node_instance: long
    :param error: Describes error.
    :type error: str
    """

    _validation = {
        'event_instance_id': {'required': True},
        'time_stamp': {'required': True},
        'kind': {'required': True},
        'node_name': {'required': True},
        'node_id': {'required': True},
        'node_instance': {'required': True},
        'error': {'required': True},
    }

    _attribute_map = {
        'event_instance_id': {'key': 'EventInstanceId', 'type': 'str'},
        'category': {'key': 'Category', 'type': 'str'},
        'time_stamp': {'key': 'TimeStamp', 'type': 'iso-8601'},
        'has_correlated_events': {'key': 'HasCorrelatedEvents', 'type': 'bool'},
        'kind': {'key': 'Kind', 'type': 'str'},
        'node_name': {'key': 'NodeName', 'type': 'str'},
        'node_id': {'key': 'NodeId', 'type': 'str'},
        'node_instance': {'key': 'NodeInstance', 'type': 'long'},
        'error': {'key': 'Error', 'type': 'str'},
    }

    def __init__(self, event_instance_id, time_stamp, node_name, node_id, node_instance, error, category=None, has_correlated_events=None):
        super(NodeCloseEvent, self).__init__(event_instance_id=event_instance_id, category=category, time_stamp=time_stamp, has_correlated_events=has_correlated_events, node_name=node_name)
        self.node_id = node_id
        self.node_instance = node_instance
        self.error = error
        self.kind = 'NodeClosed'
