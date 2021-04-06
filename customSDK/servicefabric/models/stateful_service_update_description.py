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

from .service_update_description import ServiceUpdateDescription


class StatefulServiceUpdateDescription(ServiceUpdateDescription):
    """Describes an update for a stateful service.

    All required parameters must be populated in order to send to Azure.

    :param flags: Flags indicating whether other properties are set. Each of
     the associated properties corresponds to a flag, specified below, which,
     if set, indicate that the property is specified.
     This property can be a combination of those flags obtained using bitwise
     'OR' operator.
     For example, if the provided value is 6 then the flags for
     ReplicaRestartWaitDuration (2) and QuorumLossWaitDuration (4) are set.
     - None - Does not indicate any other properties are set. The value is
     zero.
     - TargetReplicaSetSize/InstanceCount - Indicates whether the
     TargetReplicaSetSize property (for Stateful services) or the InstanceCount
     property (for Stateless services) is set. The value is 1.
     - ReplicaRestartWaitDuration - Indicates the ReplicaRestartWaitDuration
     property is set. The value is  2.
     - QuorumLossWaitDuration - Indicates the QuorumLossWaitDuration property
     is set. The value is 4.
     - StandByReplicaKeepDuration - Indicates the StandByReplicaKeepDuration
     property is set. The value is 8.
     - MinReplicaSetSize - Indicates the MinReplicaSetSize property is set. The
     value is 16.
     - PlacementConstraints - Indicates the PlacementConstraints property is
     set. The value is 32.
     - PlacementPolicyList - Indicates the ServicePlacementPolicies property is
     set. The value is 64.
     - Correlation - Indicates the CorrelationScheme property is set. The value
     is 128.
     - Metrics - Indicates the ServiceLoadMetrics property is set. The value is
     256.
     - DefaultMoveCost - Indicates the DefaultMoveCost property is set. The
     value is 512.
     - ScalingPolicy - Indicates the ScalingPolicies property is set. The value
     is 1024.
     - ServicePlacementTimeLimit - Indicates the ServicePlacementTimeLimit
     property is set. The value is 2048.
     - MinInstanceCount - Indicates the MinInstanceCount property is set. The
     value is 4096.
     - MinInstancePercentage - Indicates the MinInstancePercentage property is
     set. The value is 8192.
     - InstanceCloseDelayDuration - Indicates the InstanceCloseDelayDuration
     property is set. The value is 16384.
     - InstanceRestartWaitDuration - Indicates the InstanceCloseDelayDuration
     property is set. The value is 32768.
     - DropSourceReplicaOnMove - Indicates the DropSourceReplicaOnMove property
     is set. The value is 65536.
     - ServiceDnsName - Indicates the ServiceDnsName property is set. The value
     is 131072.
     - TagsForPlacement - Indicates the TagsForPlacement property is set. The
     value is 1048576.
     - TagsForRunning - Indicates the TagsForRunning property is set. The value
     is 2097152.
    :type flags: str
    :param placement_constraints: The placement constraints as a string.
     Placement constraints are boolean expressions on node properties and allow
     for restricting a service to particular nodes based on the service
     requirements. For example, to place a service on nodes where NodeType is
     blue specify the following: "NodeColor == blue)".
    :type placement_constraints: str
    :param correlation_scheme: The correlation scheme.
    :type correlation_scheme:
     list[~azure.servicefabric.models.ServiceCorrelationDescription]
    :param load_metrics: The service load metrics.
    :type load_metrics:
     list[~azure.servicefabric.models.ServiceLoadMetricDescription]
    :param service_placement_policies: The service placement policies.
    :type service_placement_policies:
     list[~azure.servicefabric.models.ServicePlacementPolicyDescription]
    :param default_move_cost: The move cost for the service. Possible values
     include: 'Zero', 'Low', 'Medium', 'High', 'VeryHigh'
    :type default_move_cost: str or ~azure.servicefabric.models.MoveCost
    :param scaling_policies: Scaling policies for this service.
    :type scaling_policies:
     list[~azure.servicefabric.models.ScalingPolicyDescription]
    :param service_dns_name: The DNS name of the service.
    :type service_dns_name: str
    :param tags_for_placement: Tags for placement of this service.
    :type tags_for_placement: ~azure.servicefabric.models.NodeTagsDescription
    :param tags_for_running: Tags for running of this service.
    :type tags_for_running: ~azure.servicefabric.models.NodeTagsDescription
    :param service_kind: Required. Constant filled by server.
    :type service_kind: str
    :param target_replica_set_size: The target replica set size as a number.
    :type target_replica_set_size: int
    :param min_replica_set_size: The minimum replica set size as a number.
    :type min_replica_set_size: int
    :param replica_restart_wait_duration_seconds: The duration, in seconds,
     between when a replica goes down and when a new replica is created.
    :type replica_restart_wait_duration_seconds: str
    :param quorum_loss_wait_duration_seconds: The maximum duration, in
     seconds, for which a partition is allowed to be in a state of quorum loss.
    :type quorum_loss_wait_duration_seconds: str
    :param stand_by_replica_keep_duration_seconds: The definition on how long
     StandBy replicas should be maintained before being removed.
    :type stand_by_replica_keep_duration_seconds: str
    :param service_placement_time_limit_seconds: The duration for which
     replicas can stay InBuild before reporting that build is stuck.
    :type service_placement_time_limit_seconds: str
    :param drop_source_replica_on_move: Indicates whether to drop source
     Secondary replica even if the target replica has not finished build. If
     desired behavior is to drop it as soon as possible the value of this
     property is true, if not it is false.
    :type drop_source_replica_on_move: bool
    :param replica_lifecycle_description: Defines how replicas of this service
     will behave during their lifecycle.
    :type replica_lifecycle_description:
     ~azure.servicefabric.models.ReplicaLifecycleDescription
    """

    _validation = {
        'service_kind': {'required': True},
        'target_replica_set_size': {'minimum': 1},
        'min_replica_set_size': {'minimum': 1},
    }

    _attribute_map = {
        'flags': {'key': 'Flags', 'type': 'str'},
        'placement_constraints': {'key': 'PlacementConstraints', 'type': 'str'},
        'correlation_scheme': {'key': 'CorrelationScheme', 'type': '[ServiceCorrelationDescription]'},
        'load_metrics': {'key': 'LoadMetrics', 'type': '[ServiceLoadMetricDescription]'},
        'service_placement_policies': {'key': 'ServicePlacementPolicies', 'type': '[ServicePlacementPolicyDescription]'},
        'default_move_cost': {'key': 'DefaultMoveCost', 'type': 'str'},
        'scaling_policies': {'key': 'ScalingPolicies', 'type': '[ScalingPolicyDescription]'},
        'service_dns_name': {'key': 'ServiceDnsName', 'type': 'str'},
        'tags_for_placement': {'key': 'TagsForPlacement', 'type': 'NodeTagsDescription'},
        'tags_for_running': {'key': 'TagsForRunning', 'type': 'NodeTagsDescription'},
        'service_kind': {'key': 'ServiceKind', 'type': 'str'},
        'target_replica_set_size': {'key': 'TargetReplicaSetSize', 'type': 'int'},
        'min_replica_set_size': {'key': 'MinReplicaSetSize', 'type': 'int'},
        'replica_restart_wait_duration_seconds': {'key': 'ReplicaRestartWaitDurationSeconds', 'type': 'str'},
        'quorum_loss_wait_duration_seconds': {'key': 'QuorumLossWaitDurationSeconds', 'type': 'str'},
        'stand_by_replica_keep_duration_seconds': {'key': 'StandByReplicaKeepDurationSeconds', 'type': 'str'},
        'service_placement_time_limit_seconds': {'key': 'ServicePlacementTimeLimitSeconds', 'type': 'str'},
        'drop_source_replica_on_move': {'key': 'DropSourceReplicaOnMove', 'type': 'bool'},
        'replica_lifecycle_description': {'key': 'ReplicaLifecycleDescription', 'type': 'ReplicaLifecycleDescription'},
    }

    def __init__(self, **kwargs):
        super(StatefulServiceUpdateDescription, self).__init__(**kwargs)
        self.target_replica_set_size = kwargs.get('target_replica_set_size', None)
        self.min_replica_set_size = kwargs.get('min_replica_set_size', None)
        self.replica_restart_wait_duration_seconds = kwargs.get('replica_restart_wait_duration_seconds', None)
        self.quorum_loss_wait_duration_seconds = kwargs.get('quorum_loss_wait_duration_seconds', None)
        self.stand_by_replica_keep_duration_seconds = kwargs.get('stand_by_replica_keep_duration_seconds', None)
        self.service_placement_time_limit_seconds = kwargs.get('service_placement_time_limit_seconds', None)
        self.drop_source_replica_on_move = kwargs.get('drop_source_replica_on_move', None)
        self.replica_lifecycle_description = kwargs.get('replica_lifecycle_description', None)
        self.service_kind = 'Stateful'
