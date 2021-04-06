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

from .health_evaluation import HealthEvaluation


class NodeTypeNodesHealthEvaluation(HealthEvaluation):
    """Represents health evaluation for nodes of a particular node type. The node
    type nodes evaluation can be returned when cluster health evaluation
    returns unhealthy aggregated health state, either Error or Warning. It
    contains health evaluations for each unhealthy node of the included node
    type that impacted current aggregated health state.

    All required parameters must be populated in order to send to Azure.

    :param aggregated_health_state: The health state of a Service Fabric
     entity such as Cluster, Node, Application, Service, Partition, Replica
     etc. Possible values include: 'Invalid', 'Ok', 'Warning', 'Error',
     'Unknown'
    :type aggregated_health_state: str or
     ~azure.servicefabric.models.HealthState
    :param description: Description of the health evaluation, which represents
     a summary of the evaluation process.
    :type description: str
    :param kind: Required. Constant filled by server.
    :type kind: str
    :param node_type_name: The node type name as defined in the cluster
     manifest.
    :type node_type_name: str
    :param max_percent_unhealthy_nodes: Maximum allowed percentage of
     unhealthy nodes for the node type, specified as an entry in
     NodeTypeHealthPolicyMap.
    :type max_percent_unhealthy_nodes: int
    :param total_count: Total number of nodes of the node type found in the
     health store.
    :type total_count: long
    :param unhealthy_evaluations: List of unhealthy evaluations that led to
     the aggregated health state. Includes all the unhealthy
     NodeHealthEvaluation of this node type that impacted the aggregated
     health.
    :type unhealthy_evaluations:
     list[~azure.servicefabric.models.HealthEvaluationWrapper]
    """

    _validation = {
        'kind': {'required': True},
    }

    _attribute_map = {
        'aggregated_health_state': {'key': 'AggregatedHealthState', 'type': 'str'},
        'description': {'key': 'Description', 'type': 'str'},
        'kind': {'key': 'Kind', 'type': 'str'},
        'node_type_name': {'key': 'NodeTypeName', 'type': 'str'},
        'max_percent_unhealthy_nodes': {'key': 'MaxPercentUnhealthyNodes', 'type': 'int'},
        'total_count': {'key': 'TotalCount', 'type': 'long'},
        'unhealthy_evaluations': {'key': 'UnhealthyEvaluations', 'type': '[HealthEvaluationWrapper]'},
    }

    def __init__(self, **kwargs):
        super(NodeTypeNodesHealthEvaluation, self).__init__(**kwargs)
        self.node_type_name = kwargs.get('node_type_name', None)
        self.max_percent_unhealthy_nodes = kwargs.get('max_percent_unhealthy_nodes', None)
        self.total_count = kwargs.get('total_count', None)
        self.unhealthy_evaluations = kwargs.get('unhealthy_evaluations', None)
        self.kind = 'NodeTypeNodes'