# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Custom commands for the Service Fabric partition support"""

def start_data_loss(client, service_id, partition_id, operation_id, data_loss_mode, timeout=60):
    """This API will induce data loss for the specified partition. It will trigger a call to the
    OnDataLossAsync API of the partition.

    This API will induce data loss for the specified partition. It will trigger a call to the
    OnDataLoss API of the partition.
    Actual data loss will depend on the specified DataLossMode.


    * PartialDataLoss - Only a quorum of replicas are removed and OnDataLoss is triggered for the
    partition but actual data loss depends on the presence of in-flight replication.
    * FullDataLoss - All replicas are removed hence all data is lost and OnDataLoss is triggered.

    This API should only be called with a stateful service as the target.

    Calling this API with a system service as the target is not advised.

    Note:  Once this API has been called, it cannot be reversed. Calling CancelOperation will only
    stop execution and clean up internal system state.
    It will not restore data if the command has progressed far enough to cause data loss.

    Call the GetDataLossProgress API with the same OperationId to return information on the
    operation started with this API.

    :param service_id: The identity of the service. This ID is typically the full name of the
        service without the 'fabric:' URI scheme.
        Starting from version 6.0, hierarchical names are delimited with the "~" character.
        For example, if the service name is "fabric:/myapp/app1/svc1", the service identity would be
        "myapp~app1~svc1" in 6.0+ and "myapp/app1/svc1" in previous versions.
    :type service_id: str
    :param partition_id: The identity of the partition.
    :type partition_id: str
    :param operation_id: A GUID that identifies a call of this API.  This is passed into the
        corresponding GetProgress API.
    :paramtype operation_id: str
    :param data_loss_mode: This enum is passed to the StartDataLoss API to indicate what type of
        data loss to induce. Known values are: "Invalid", "PartialDataLoss", and "FullDataLoss".
    :paramtype data_loss_mode: str
    """

    return client.start_data_loss(service_id, partition_id, operation_id=operation_id, data_loss_mode=data_loss_mode, timeout=timeout)

def get_data_loss_progress(client, service_id, partition_id, operation_id, timeout=60):
    """Gets the progress of a partition data loss operation started using the StartDataLoss API.

    Gets the progress of a data loss operation started with StartDataLoss, using the OperationId.

    :param service_id: The identity of the service. This ID is typically the full name of the
        service without the 'fabric:' URI scheme.
        Starting from version 6.0, hierarchical names are delimited with the "~" character.
        For example, if the service name is "fabric:/myapp/app1/svc1", the service identity would be
        "myapp~app1~svc1" in 6.0+ and "myapp/app1/svc1" in previous versions.
    :type service_id: str
    :param partition_id: The identity of the partition.
    :type partition_id: str
    :param operation_id: A GUID that identifies a call of this API.  This is passed into the
        corresponding GetProgress API.
    :paramtype operation_id: str
    """

    return client.get_data_loss_progress(service_id, partition_id, operation_id=operation_id, timeout=timeout)

def get_loaded_partition_info_list(client, metric_name, service_name=None, ordering=None, max_results=0, continuation_token=None, timeout=60):
    """Gets ordered list of partitions.

    Retrieves partitions which are most/least loaded according to specified metric.

    :param metric_name: Name of the metric based on which to get ordered list of partitions.
    :paramtype metric_name: str
    :param service_name: The name of a service. Default value is None.
    :paramtype service_name: str
    :param ordering: Ordering of partitions' load. Known values are: "Desc" or "Asc". Default
        value is None.
    :paramtype ordering: str
    :param max_results: The maximum number of results to be returned as part of the paged
        queries. This parameter defines the upper bound on the number of results returned. The results
        returned can be less than the specified maximum results if they do not fit in the message as
        per the max message size restrictions defined in the configuration. If this parameter is zero
        or not specified, the paged query includes as many results as possible that fit in the return
        message. Default value is 0.
    :paramtype max_results: long
    :param continuation_token: The continuation token parameter is used to obtain next
        set of results. A continuation token with a non-empty value is included in the response of the
        API when the results from the system do not fit in a single response. When this value is passed
        to the next API call, the API returns next set of results. If there are no further results,
        then the continuation token does not contain a value. The value of this parameter should not be
        URL encoded. Default value is None.
        """

    return client.get_loaded_partition_info_list(metric_name=metric_name, continuation_token_parameter=continuation_token,
                                         service_name=service_name, ordering=ordering, max_results=max_results, timeout=60)

def get_partition_health(client, partition_id, events_health_state_filter=0, replicas_health_state_filter=0, exclude_health_statistics=False, timeout=60):
    """Gets the health of the specified Service Fabric partition.

    Use EventsHealthStateFilter to filter the collection of health events reported on the service
    based on the health state.
    Use ReplicasHealthStateFilter to filter the collection of ReplicaHealthState objects on the
    partition.
    If you specify a partition that does not exist in the health store, this request returns an
    error.

    :param partition_id: The identity of the partition.
    :type partition_id: str
    :param events_health_state_filter: Allows filtering the collection of HealthEvent objects
        returned based on health state.
        The possible values for this parameter include integer value of one of the following health
        states.
        Only events that match the filter are returned. All events are used to evaluate the aggregated
        health state.
        If not specified, all entries are returned. The state values are flag-based enumeration, so
        the value could be a combination of these values, obtained using the bitwise 'OR' operator. For
        example, If the provided value is 6 then all of the events with HealthState value of OK (2) and
        Warning (4) are returned.


        * Default - Default value. Matches any HealthState. The value is zero.
        * None - Filter that doesn't match any HealthState value. Used in order to return no results
        on a given collection of states. The value is 1.
        * Ok - Filter that matches input with HealthState value Ok. The value is 2.
        * Warning - Filter that matches input with HealthState value Warning. The value is 4.
        * Error - Filter that matches input with HealthState value Error. The value is 8.
        * All - Filter that matches input with any HealthState value. The value is 65535. Default
        value is 0.
    :paramtype events_health_state_filter: int
    :param replicas_health_state_filter: Allows filtering the collection of ReplicaHealthState
        objects on the partition. The value can be obtained from members or bitwise operations on
        members of HealthStateFilter. Only replicas that match the filter will be returned. All
        replicas will be used to evaluate the aggregated health state. If not specified, all entries
        will be returned.The state values are flag-based enumeration, so the value could be a
        combination of these values obtained using bitwise 'OR' operator. For example, If the provided
        value is 6 then all of the events with HealthState value of OK (2) and Warning (4) will be
        returned. The possible values for this parameter include integer value of one of the following
        health states.


        * Default - Default value. Matches any HealthState. The value is zero.
        * None - Filter that doesn't match any HealthState value. Used in order to return no results
        on a given collection of states. The value is 1.
        * Ok - Filter that matches input with HealthState value Ok. The value is 2.
        * Warning - Filter that matches input with HealthState value Warning. The value is 4.
        * Error - Filter that matches input with HealthState value Error. The value is 8.
        * All - Filter that matches input with any HealthState value. The value is 65535. Default
        value is 0.
    :paramtype replicas_health_state_filter: int
    :param exclude_health_statistics: Indicates whether the health statistics should be returned
        as part of the query result. False by default.
        The statistics show the number of children entities in health state Ok, Warning, and Error.
        Default value is False.
    :paramtype exclude_health_statistics: bool
    """

    return client.get_partition_health(partition_id, events_health_state_filter=events_health_state_filter, replicas_health_state_filter=replicas_health_state_filter,
                                exclude_health_statistics=exclude_health_statistics, timeout=timeout)


def get_partition_info_list(client, service_id, continuation_token=None, timeout=60):
    """Gets the list of partitions of a Service Fabric service.

    The response includes the partition ID, partitioning scheme information, keys supported by the
    partition, status, health, and other details about the partition.

    :param service_id: The identity of the service. This ID is typically the full name of the
        service without the 'fabric:' URI scheme.
        Starting from version 6.0, hierarchical names are delimited with the "~" character.
        For example, if the service name is "fabric:/myapp/app1/svc1", the service identity would be
        "myapp~app1~svc1" in 6.0+ and "myapp/app1/svc1" in previous versions.
    :type service_id: str
    :param continuation_token: The continuation token parameter is used to obtain next
        set of results. A continuation token with a non-empty value is included in the response of the
        API when the results from the system do not fit in a single response. When this value is passed
        to the next API call, the API returns next set of results. If there are no further results,
        then the continuation token does not contain a value. The value of this parameter should not be
        URL encoded. Default value is None.
    :paramtype continuation_token: str
    """
    return client.get_partition_info_list(service_id, continuation_token_parameter=continuation_token, timeout=timeout)

def move_instance(client, service_id, partition_id, current_node_name=None, new_node_name=None, ignore_constraints=False, timeout=60):
    """Moves the instance of a partition of a stateless service.

    This command moves the instance of a partition of a stateless service, respecting all
    constraints.
    Partition id and service name must be specified to be able to move the instance.
    CurrentNodeName when specified identifies the instance that is moved. If not specified, random
    instance will be moved
    New node name can be omitted, and in that case instance is moved to a random node.
    If IgnoreConstraints parameter is specified and set to true, then instance will be moved
    regardless of the constraints.

    :param service_id: The identity of the service. This ID is typically the full name of the
        service without the 'fabric:' URI scheme.
        Starting from version 6.0, hierarchical names are delimited with the "~" character.
        For example, if the service name is "fabric:/myapp/app1/svc1", the service identity would be
        "myapp~app1~svc1" in 6.0+ and "myapp/app1/svc1" in previous versions.
    :type service_id: str
    :param partition_id: The identity of the partition.
    :type partition_id: str
    :param current_node_name: The name of the source node for instance move. If not specified,
        instance is moved from a random node. Default value is None.
    :paramtype current_node_name: str
    :param new_node_name: The name of the target node for secondary replica or instance move. If
        not specified, replica or instance is moved to a random node. Default value is None.
    :paramtype new_node_name: str
    :param ignore_constraints: Ignore constraints when moving a replica or instance. If this
        parameter is not specified, all constraints are honored. Default value is False.
    :paramtype ignore_constraints: bool
    """
    return client.move_instance(service_id, partition_id, current_node_name=current_node_name, new_node_name=new_node_name,
                         ignore_constraints=ignore_constraints, timeout=timeout)

def move_primary_replica(client, partition_id, node_name=None, ignore_constraints=False, timeout=60):
    """Moves the primary replica of a partition of a stateful service.

    This command moves the primary replica of a partition of a stateful service, respecting all
    constraints.
    If NodeName parameter is specified, primary will be moved to the specified node (if constraints
    allow it).
    If NodeName parameter is not specified, primary replica will be moved to a random node in the
    cluster.
    If IgnoreConstraints parameter is specified and set to true, then primary will be moved
    regardless of the constraints.

    :param partition_id: The identity of the partition.
    :type partition_id: str
    :param node_name: The name of the node. Default value is None.
    :paramtype node_name: str
    :param ignore_constraints: Ignore constraints when moving a replica or instance. If this
        parameter is not specified, all constraints are honored. Default value is False.
    :paramtype ignore_constraints: bool
    """
    return client.move_primary_replica(partition_id, node_name=node_name, ignore_constraints=ignore_constraints, timeout=timeout)

def move_secondary_replica(client, partition_id, current_node_name, new_node_name=None, ignore_constraints=False, timeout=60):
    """Moves the secondary replica of a partition of a stateful service.

    This command moves the secondary replica of a partition of a stateful service, respecting all
    constraints.
    CurrentNodeName parameter must be specified to identify the replica that is moved.
    Source node name must be specified, but new node name can be omitted, and in that case replica
    is moved to a random node.
    If IgnoreConstraints parameter is specified and set to true, then secondary will be moved
    regardless of the constraints.

    :param partition_id: The identity of the partition.
    :type partition_id: str
    :param current_node_name: The name of the source node for secondary replica move.
    :paramtype current_node_name: str
    :param new_node_name: The name of the target node for secondary replica or instance move. If
        not specified, replica or instance is moved to a random node. Default value is None.
    :paramtype new_node_name: str
    :param ignore_constraints: Ignore constraints when moving a replica or instance. If this
        parameter is not specified, all constraints are honored. Default value is False.
    :paramtype ignore_constraints: bool
    :param timeout: The server timeout for performing the operation in seconds. This timeout
        specifies the time duration that the client is willing to wait for the requested operation to
        complete. The default value for this parameter is 60 seconds. Default value is 60.
        """
    return client.move_secondary_replica(partition_id, current_node_name=current_node_name, new_node_name=new_node_name,
                                  ignore_constraints=ignore_constraints, timeout=timeout)

def start_quorum_loss(client, service_id, partition_id, operation_id, quorum_loss_mode, quorum_loss_duration, timeout=60):
    """Induces quorum loss for a given stateful service partition.

    This API is useful for a temporary quorum loss situation on your service.

    Call the GetQuorumLossProgress API with the same OperationId to return information on the
    operation started with this API.

    This can only be called on stateful persisted (HasPersistedState==true) services.  Do not use
    this API on stateless services or stateful in-memory only services.

    :param service_id: The identity of the service. This ID is typically the full name of the
        service without the 'fabric:' URI scheme.
        Starting from version 6.0, hierarchical names are delimited with the "~" character.
        For example, if the service name is "fabric:/myapp/app1/svc1", the service identity would be
        "myapp~app1~svc1" in 6.0+ and "myapp/app1/svc1" in previous versions.
    :type service_id: str
    :param partition_id: The identity of the partition.
    :type partition_id: str
    :param operation_id: A GUID that identifies a call of this API.  This is passed into the
        corresponding GetProgress API.
    :paramtype operation_id: str
    :param quorum_loss_mode: This enum is passed to the StartQuorumLoss API to indicate what type
        of quorum loss to induce. Known values are: "Invalid", "QuorumReplicas", and "AllReplicas".
    :paramtype quorum_loss_mode: str
    :param quorum_loss_duration: The amount of time for which the partition will be kept in
        quorum loss.  This must be specified in seconds.
    :paramtype quorum_loss_duration: int
    """
    client.start_quorum_loss(service_id, partition_id, operation_id=operation_id, 
    quorum_loss_mode=quorum_loss_mode, quorum_loss_duration=quorum_loss_duration, timeout=timeout)

def get_quorum_loss_progress(client, service_id, partition_id, operation_id, timeout=60):
    """Gets the progress of a quorum loss operation on a partition started using the StartQuorumLoss
    API.

    Gets the progress of a quorum loss operation started with StartQuorumLoss, using the provided
    OperationId.

    :param service_id: The identity of the service. This ID is typically the full name of the
        service without the 'fabric:' URI scheme.
        Starting from version 6.0, hierarchical names are delimited with the "~" character.
        For example, if the service name is "fabric:/myapp/app1/svc1", the service identity would be
        "myapp~app1~svc1" in 6.0+ and "myapp/app1/svc1" in previous versions.
    :type service_id: str
    :param partition_id: The identity of the partition.
    :type partition_id: str
    :param operation_id: A GUID that identifies a call of this API.  This is passed into the
        corresponding GetProgress API.
    :paramtype operation_id: str
    """
    return client.get_quorum_loss_progress(service_id, partition_id, operation_id=operation_id, timeout=timeout)

def start_partition_restart(client, service_id, partition_id, operation_id, restart_partition_mode, timeout=60):
    """This API will restart some or all replicas or instances of the specified partition.

    This API is useful for testing failover.

    If used to target a stateless service partition, RestartPartitionMode must be
    AllReplicasOrInstances.

    Call the GetPartitionRestartProgress API using the same OperationId to get the progress.

    :param service_id: The identity of the service. This ID is typically the full name of the
        service without the 'fabric:' URI scheme.
        Starting from version 6.0, hierarchical names are delimited with the "~" character.
        For example, if the service name is "fabric:/myapp/app1/svc1", the service identity would be
        "myapp~app1~svc1" in 6.0+ and "myapp/app1/svc1" in previous versions.
    :type service_id: str
    :param partition_id: The identity of the partition.
    :type partition_id: str
    :param operation_id: A GUID that identifies a call of this API.  This is passed into the
        corresponding GetProgress API.
    :paramtype operation_id: str
    :param restart_partition_mode: Describe which partitions to restart. Known values are:
        "Invalid", "AllReplicasOrInstances", and "OnlyActiveSecondaries".
    :paramtype restart_partition_mode: str
    """
    client.start_partition_restart(service_id, partition_id, operation_id=operation_id, 
                                   restart_partition_mode=restart_partition_mode, timeout=timeout)

def get_partition_restart_progress(client, service_id, partition_id, operation_id, timeout=60):
    """Gets the progress of a PartitionRestart operation started using StartPartitionRestart.

    Gets the progress of a PartitionRestart started with StartPartitionRestart using the provided
    OperationId.

    :param service_id: The identity of the service. This ID is typically the full name of the
        service without the 'fabric:' URI scheme.
        Starting from version 6.0, hierarchical names are delimited with the "~" character.
        For example, if the service name is "fabric:/myapp/app1/svc1", the service identity would be
        "myapp~app1~svc1" in 6.0+ and "myapp/app1/svc1" in previous versions.
    :type service_id: str
    :param partition_id: The identity of the partition.
    :type partition_id: str
    :param operation_id: A GUID that identifies a call of this API.  This is passed into the
        corresponding GetProgress API.
    :paramtype operation_id: str
    :param timeout: The server timeout for performing the operation in seconds. This timeout
        specifies the time duration that the client is willing to wait for the requested operation to
        complete. The default value for this parameter is 60 seconds. Default value is 60.
        """
    return client.get_partition_restart_progress(service_id, partition_id, operation_id=operation_id, timeout=timeout)