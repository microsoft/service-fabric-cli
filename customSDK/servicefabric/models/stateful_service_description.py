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

from .service_description import ServiceDescription


class StatefulServiceDescription(ServiceDescription):
    """Describes a stateful service.

    All required parameters must be populated in order to send to Azure.

    :param application_name: The name of the application, including the
     'fabric:' URI scheme.
    :type application_name: str
    :param service_name: Required. The full name of the service with 'fabric:'
     URI scheme.
    :type service_name: str
    :param service_type_name: Required. Name of the service type as specified
     in the service manifest.
    :type service_type_name: str
    :param initialization_data: The initialization data as an array of bytes.
     Initialization data is passed to service instances or replicas when they
     are created.
    :type initialization_data: list[int]
    :param partition_description: Required. The partition description as an
     object.
    :type partition_description:
     ~azure.servicefabric.models.PartitionSchemeDescription
    :param placement_constraints: The placement constraints as a string.
     Placement constraints are boolean expressions on node properties and allow
     for restricting a service to particular nodes based on the service
     requirements. For example, to place a service on nodes where NodeType is
     blue specify the following: "NodeColor == blue)".
    :type placement_constraints: str
    :param correlation_scheme: The correlation scheme.
    :type correlation_scheme:
     list[~azure.servicefabric.models.ServiceCorrelationDescription]
    :param service_load_metrics: The service load metrics.
    :type service_load_metrics:
     list[~azure.servicefabric.models.ServiceLoadMetricDescription]
    :param service_placement_policies: The service placement policies.
    :type service_placement_policies:
     list[~azure.servicefabric.models.ServicePlacementPolicyDescription]
    :param default_move_cost: The move cost for the service. Possible values
     include: 'Zero', 'Low', 'Medium', 'High', 'VeryHigh'
    :type default_move_cost: str or ~azure.servicefabric.models.MoveCost
    :param is_default_move_cost_specified: Indicates if the DefaultMoveCost
     property is specified.
    :type is_default_move_cost_specified: bool
    :param service_package_activation_mode: The activation mode of service
     package to be used for a service. Possible values include:
     'SharedProcess', 'ExclusiveProcess'
    :type service_package_activation_mode: str or
     ~azure.servicefabric.models.ServicePackageActivationMode
    :param service_dns_name: The DNS name of the service. It requires the DNS
     system service to be enabled in Service Fabric cluster.
    :type service_dns_name: str
    :param scaling_policies: Scaling policies for this service.
    :type scaling_policies:
     list[~azure.servicefabric.models.ScalingPolicyDescription]
    :param tags_required_to_place: Tags for placement of this service.
    :type tags_required_to_place:
     ~azure.servicefabric.models.NodeTagsDescription
    :param tags_required_to_run: Tags for running of this service.
    :type tags_required_to_run:
     ~azure.servicefabric.models.NodeTagsDescription
    :param service_kind: Required. Constant filled by server.
    :type service_kind: str
    :param target_replica_set_size: Required. The target replica set size as a
     number.
    :type target_replica_set_size: int
    :param min_replica_set_size: Required. The minimum replica set size as a
     number.
    :type min_replica_set_size: int
    :param has_persisted_state: Required. A flag indicating whether this is a
     persistent service which stores states on the local disk. If it is then
     the value of this property is true, if not it is false.
    :type has_persisted_state: bool
    :param flags: Flags indicating whether other properties are set. Each of
     the associated properties corresponds to a flag, specified below, which,
     if set, indicate that the property is specified.
     This property can be a combination of those flags obtained using bitwise
     'OR' operator.
     For example, if the provided value is 6 then the flags for
     QuorumLossWaitDuration (2) and StandByReplicaKeepDuration(4) are set.
     - None - Does not indicate any other properties are set. The value is
     zero.
     - ReplicaRestartWaitDuration - Indicates the ReplicaRestartWaitDuration
     property is set. The value is 1.
     - QuorumLossWaitDuration - Indicates the QuorumLossWaitDuration property
     is set. The value is 2.
     - StandByReplicaKeepDuration - Indicates the StandByReplicaKeepDuration
     property is set. The value is 4.
     - ServicePlacementTimeLimit - Indicates the ServicePlacementTimeLimit
     property is set. The value is 8.
     - DropSourceReplicaOnMove - Indicates the DropSourceReplicaOnMove property
     is set. The value is 16.
    :type flags: int
    :param replica_restart_wait_duration_seconds: The duration, in seconds,
     between when a replica goes down and when a new replica is created.
    :type replica_restart_wait_duration_seconds: long
    :param quorum_loss_wait_duration_seconds: The maximum duration, in
     seconds, for which a partition is allowed to be in a state of quorum loss.
    :type quorum_loss_wait_duration_seconds: long
    :param stand_by_replica_keep_duration_seconds: The definition on how long
     StandBy replicas should be maintained before being removed.
    :type stand_by_replica_keep_duration_seconds: long
    :param service_placement_time_limit_seconds: The duration for which
     replicas can stay InBuild before reporting that build is stuck.
    :type service_placement_time_limit_seconds: long
    :param drop_source_replica_on_move: Indicates whether to drop source
     Secondary replica even if the target replica has not finished build. If
     desired behavior is to drop it as soon as possible the value of this
     property is true, if not it is false.
    :type drop_source_replica_on_move: bool
    :param replica_lifecycle_description: Defines how replicas of this service
     will behave during ther lifecycle.
    :type replica_lifecycle_description:
     ~azure.servicefabric.models.ReplicaLifecycleDescription
    :param auxiliary_replica_count: The auxiliary replica count as a number.
     To use Auxiliary replicas, the following must be true:
     AuxiliaryReplicaCount < (TargetReplicaSetSize+1)/2 and
     TargetReplicaSetSize >=3.
    :type auxiliary_replica_count: int
    """

    _validation = {
        'service_name': {'required': True},
        'service_type_name': {'required': True},
        'partition_description': {'required': True},
        'service_kind': {'required': True},
        'target_replica_set_size': {'required': True, 'minimum': 1},
        'min_replica_set_size': {'required': True, 'minimum': 1},
        'has_persisted_state': {'required': True},
        'replica_restart_wait_duration_seconds': {'maximum': 4294967295, 'minimum': 0},
        'quorum_loss_wait_duration_seconds': {'maximum': 4294967295, 'minimum': 0},
        'stand_by_replica_keep_duration_seconds': {'maximum': 4294967295, 'minimum': 0},
        'service_placement_time_limit_seconds': {'maximum': 4294967295, 'minimum': 0},
        'auxiliary_replica_count': {'minimum': 0},
    }

    _attribute_map = {
        'application_name': {'key': 'ApplicationName', 'type': 'str'},
        'service_name': {'key': 'ServiceName', 'type': 'str'},
        'service_type_name': {'key': 'ServiceTypeName', 'type': 'str'},
        'initialization_data': {'key': 'InitializationData', 'type': '[int]'},
        'partition_description': {'key': 'PartitionDescription', 'type': 'PartitionSchemeDescription'},
        'placement_constraints': {'key': 'PlacementConstraints', 'type': 'str'},
        'correlation_scheme': {'key': 'CorrelationScheme', 'type': '[ServiceCorrelationDescription]'},
        'service_load_metrics': {'key': 'ServiceLoadMetrics', 'type': '[ServiceLoadMetricDescription]'},
        'service_placement_policies': {'key': 'ServicePlacementPolicies', 'type': '[ServicePlacementPolicyDescription]'},
        'default_move_cost': {'key': 'DefaultMoveCost', 'type': 'str'},
        'is_default_move_cost_specified': {'key': 'IsDefaultMoveCostSpecified', 'type': 'bool'},
        'service_package_activation_mode': {'key': 'ServicePackageActivationMode', 'type': 'str'},
        'service_dns_name': {'key': 'ServiceDnsName', 'type': 'str'},
        'scaling_policies': {'key': 'ScalingPolicies', 'type': '[ScalingPolicyDescription]'},
        'tags_required_to_place': {'key': 'TagsRequiredToPlace', 'type': 'NodeTagsDescription'},
        'tags_required_to_run': {'key': 'TagsRequiredToRun', 'type': 'NodeTagsDescription'},
        'service_kind': {'key': 'ServiceKind', 'type': 'str'},
        'target_replica_set_size': {'key': 'TargetReplicaSetSize', 'type': 'int'},
        'min_replica_set_size': {'key': 'MinReplicaSetSize', 'type': 'int'},
        'has_persisted_state': {'key': 'HasPersistedState', 'type': 'bool'},
        'flags': {'key': 'Flags', 'type': 'int'},
        'replica_restart_wait_duration_seconds': {'key': 'ReplicaRestartWaitDurationSeconds', 'type': 'long'},
        'quorum_loss_wait_duration_seconds': {'key': 'QuorumLossWaitDurationSeconds', 'type': 'long'},
        'stand_by_replica_keep_duration_seconds': {'key': 'StandByReplicaKeepDurationSeconds', 'type': 'long'},
        'service_placement_time_limit_seconds': {'key': 'ServicePlacementTimeLimitSeconds', 'type': 'long'},
        'drop_source_replica_on_move': {'key': 'DropSourceReplicaOnMove', 'type': 'bool'},
        'replica_lifecycle_description': {'key': 'ReplicaLifecycleDescription', 'type': 'ReplicaLifecycleDescription'},
        'auxiliary_replica_count': {'key': 'AuxiliaryReplicaCount', 'type': 'int'},
    }

    def __init__(self, **kwargs):
        super(StatefulServiceDescription, self).__init__(**kwargs)
        self.target_replica_set_size = kwargs.get('target_replica_set_size', None)
        self.min_replica_set_size = kwargs.get('min_replica_set_size', None)
        self.has_persisted_state = kwargs.get('has_persisted_state', None)
        self.flags = kwargs.get('flags', None)
        self.replica_restart_wait_duration_seconds = kwargs.get('replica_restart_wait_duration_seconds', None)
        self.quorum_loss_wait_duration_seconds = kwargs.get('quorum_loss_wait_duration_seconds', None)
        self.stand_by_replica_keep_duration_seconds = kwargs.get('stand_by_replica_keep_duration_seconds', None)
        self.service_placement_time_limit_seconds = kwargs.get('service_placement_time_limit_seconds', None)
        self.drop_source_replica_on_move = kwargs.get('drop_source_replica_on_move', None)
        self.replica_lifecycle_description = kwargs.get('replica_lifecycle_description', None)
        self.auxiliary_replica_count = kwargs.get('auxiliary_replica_count', None)
        self.service_kind = 'Stateful'
