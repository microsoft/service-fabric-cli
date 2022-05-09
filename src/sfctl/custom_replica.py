# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------

def get_replica_info_list(client, partition_id, continuation_token=None, timeout=60):
    """Gets the information about replicas of a Service Fabric service partition.

    The GetReplicas endpoint returns information about the replicas of the specified partition. The
    response includes the ID, role, status, health, node name, uptime, and other details about the
    replica.

    :param partition_id: The identity of the partition.
    :type partition_id: str
    :param continuation_token: The continuation token parameter is used to obtain next
        set of results. A continuation token with a non-empty value is included in the response of the
        API when the results from the system do not fit in a single response. When this value is passed
        to the next API call, the API returns next set of results. If there are no further results,
        then the continuation token does not contain a value. The value of this parameter should not be
        URL encoded. Default value is None.
    :paramtype continuation_token: str
    """
    return client.get_replica_info_list(partition_id, continuation_token_parameter=continuation_token, timeout=timeout)

def get_deployed_service_replica_info_list(client, node_name, application_id, partition_id=None, service_manifest_name=None, timeout=60):
    """Gets the list of replicas deployed on a Service Fabric node.
    Gets the list containing the information about replicas deployed on a Service Fabric node. The
    information include partition ID, replica ID, status of the replica, name of the service, name
    of the service type, and other information. Use PartitionId or ServiceManifestName query
    parameters to return information about the deployed replicas matching the specified values for
    those parameters.

    :param node_name: The name of the node.
    :type node_name: str
    :param application_id: The identity of the application. This is typically the full name of the
        application without the 'fabric:' URI scheme.
        Starting from version 6.0, hierarchical names are delimited with the "~" character.
        For example, if the application name is "fabric:/myapp/app1", the application identity would
        be "myapp~app1" in 6.0+ and "myapp/app1" in previous versions.
    :type application_id: str
    :param partition_id: The identity of the partition. Default value is None.
    :paramtype partition_id: str
    :param service_manifest_name: The name of a service manifest registered as part of an
        application type in a Service Fabric cluster. Default value is None.
    :paramtype service_manifest_name: str
    :param timeout: The server timeout for performing the operation in seconds. This timeout
        specifies the time duration that the client is willing to wait for the requested operation to
        complete. The default value for this parameter is 60 seconds. Default value is 60.\
            """

    return client.get_deployed_service_replica_info_list(node_name, application_id, partition_id=partition_id,
                                                service_manifest_name=service_manifest_name, timeout=timeout)

def get_replica_health(client, partition_id, replica_id, events_health_state_filter=0, timeout=60):
    """Gets the health of a Service Fabric stateful service replica or stateless service instance.

    Gets the health of a Service Fabric replica.
    Use EventsHealthStateFilter to filter the collection of health events reported on the replica
    based on the health state.

    :param partition_id: The identity of the partition.
    :type partition_id: str
    :param replica_id: The identifier of the replica.
    :type replica_id: str
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
    """
    return client.get_replica_health(partition_id, replica_id, events_health_state_filter=events_health_state_filter, timeout=timeout)

def remove_replica(client, node_name, partition_id, replica_id, force_remove=None, timeout=60):
    """Removes a service replica running on a node.

    This API simulates a Service Fabric replica failure by removing a replica from a Service Fabric
    cluster. The removal closes the replica, transitions the replica to the role None, and then
    removes all of the state information of the replica from the cluster. This API tests the
    replica state removal path, and simulates the report fault permanent path through client APIs.
    Warning - There are no safety checks performed when this API is used. Incorrect use of this API
    can lead to data loss for stateful services. In addition, the forceRemove flag impacts all
    other replicas hosted in the same process.

    :param node_name: The name of the node.
    :type node_name: str
    :param partition_id: The identity of the partition.
    :type partition_id: str
    :param replica_id: The identifier of the replica.
    :type replica_id: str
    :param force_remove: Remove a Service Fabric application or service forcefully without going
        through the graceful shutdown sequence. This parameter can be used to forcefully delete an
        application or service for which delete is timing out due to issues in the service code that
        prevents graceful close of replicas. Default value is None.
    :paramtype force_remove: bool
    """
    return client.remove_replica(node_name, partition_id, replica_id, force_remove=force_remove, timeout=timeout)