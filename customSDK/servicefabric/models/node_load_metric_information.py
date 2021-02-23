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


class NodeLoadMetricInformation(Model):
    """Represents data structure that contains load information for a certain
    metric on a node.

    :param name: Name of the metric for which this load information is
     provided.
    :type name: str
    :param node_capacity: Total capacity on the node for this metric.
    :type node_capacity: str
    :param node_load: Current load on the node for this metric. In future
     releases of Service Fabric this parameter will be deprecated in favor of
     CurrentNodeLoad.
    :type node_load: str
    :param node_remaining_capacity: The remaining capacity on the node for
     this metric. In future releases of Service Fabric this parameter will be
     deprecated in favor of NodeCapacityRemaining.
    :type node_remaining_capacity: str
    :param is_capacity_violation: Indicates if there is a capacity violation
     for this metric on the node.
    :type is_capacity_violation: bool
    :param node_buffered_capacity: The value that indicates the reserved
     capacity for this metric on the node.
    :type node_buffered_capacity: str
    :param node_remaining_buffered_capacity: The remaining reserved capacity
     for this metric on the node. In future releases of Service Fabric this
     parameter will be deprecated in favor of BufferedNodeCapacityRemaining.
    :type node_remaining_buffered_capacity: str
    :param current_node_load: Current load on the node for this metric.
    :type current_node_load: str
    :param node_capacity_remaining: The remaining capacity on the node for the
     metric.
    :type node_capacity_remaining: str
    :param buffered_node_capacity_remaining: The remaining capacity which is
     not reserved by NodeBufferPercentage for this metric on the node.
    :type buffered_node_capacity_remaining: str
    :param planned_node_load_removal: This value represents the load of the
     replicas that are planned to be removed in the future.
     This kind of load is reported for replicas that are currently being moving
     to other nodes and for replicas that are currently being dropped but still
     use the load on the source node.
    :type planned_node_load_removal: str
    """

    _attribute_map = {
        'name': {'key': 'Name', 'type': 'str'},
        'node_capacity': {'key': 'NodeCapacity', 'type': 'str'},
        'node_load': {'key': 'NodeLoad', 'type': 'str'},
        'node_remaining_capacity': {'key': 'NodeRemainingCapacity', 'type': 'str'},
        'is_capacity_violation': {'key': 'IsCapacityViolation', 'type': 'bool'},
        'node_buffered_capacity': {'key': 'NodeBufferedCapacity', 'type': 'str'},
        'node_remaining_buffered_capacity': {'key': 'NodeRemainingBufferedCapacity', 'type': 'str'},
        'current_node_load': {'key': 'CurrentNodeLoad', 'type': 'str'},
        'node_capacity_remaining': {'key': 'NodeCapacityRemaining', 'type': 'str'},
        'buffered_node_capacity_remaining': {'key': 'BufferedNodeCapacityRemaining', 'type': 'str'},
        'planned_node_load_removal': {'key': 'PlannedNodeLoadRemoval', 'type': 'str'},
    }

    def __init__(self, **kwargs):
        super(NodeLoadMetricInformation, self).__init__(**kwargs)
        self.name = kwargs.get('name', None)
        self.node_capacity = kwargs.get('node_capacity', None)
        self.node_load = kwargs.get('node_load', None)
        self.node_remaining_capacity = kwargs.get('node_remaining_capacity', None)
        self.is_capacity_violation = kwargs.get('is_capacity_violation', None)
        self.node_buffered_capacity = kwargs.get('node_buffered_capacity', None)
        self.node_remaining_buffered_capacity = kwargs.get('node_remaining_buffered_capacity', None)
        self.current_node_load = kwargs.get('current_node_load', None)
        self.node_capacity_remaining = kwargs.get('node_capacity_remaining', None)
        self.buffered_node_capacity_remaining = kwargs.get('buffered_node_capacity_remaining', None)
        self.planned_node_load_removal = kwargs.get('planned_node_load_removal', None)
