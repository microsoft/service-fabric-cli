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

from .health_evaluation_py3 import HealthEvaluation


class ReplicasHealthEvaluation(HealthEvaluation):
    """Represents health evaluation for replicas, containing health evaluations
    for each unhealthy replica that impacted current aggregated health state.
    Can be returned when evaluating partition health and the aggregated health
    state is either Error or Warning.

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
    :param max_percent_unhealthy_replicas_per_partition: Maximum allowed
     percentage of unhealthy replicas per partition from the
     ApplicationHealthPolicy.
    :type max_percent_unhealthy_replicas_per_partition: int
    :param total_count: Total number of replicas in the partition from the
     health store.
    :type total_count: long
    :param unhealthy_evaluations: List of unhealthy evaluations that led to
     the aggregated health state. Includes all the unhealthy
     ReplicaHealthEvaluation that impacted the aggregated health.
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
        'max_percent_unhealthy_replicas_per_partition': {'key': 'MaxPercentUnhealthyReplicasPerPartition', 'type': 'int'},
        'total_count': {'key': 'TotalCount', 'type': 'long'},
        'unhealthy_evaluations': {'key': 'UnhealthyEvaluations', 'type': '[HealthEvaluationWrapper]'},
    }

    def __init__(self, *, aggregated_health_state=None, description: str=None, max_percent_unhealthy_replicas_per_partition: int=None, total_count: int=None, unhealthy_evaluations=None, **kwargs) -> None:
        super(ReplicasHealthEvaluation, self).__init__(aggregated_health_state=aggregated_health_state, description=description, **kwargs)
        self.max_percent_unhealthy_replicas_per_partition = max_percent_unhealthy_replicas_per_partition
        self.total_count = total_count
        self.unhealthy_evaluations = unhealthy_evaluations
        self.kind = 'Replicas'
