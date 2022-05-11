# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Commands related to Service Fabric Node commands for node tagging"""

def add_node_tags(client, node_name, tags):
    """Add the corresponding tags to a node"""

    client.add_node_tags(node_name, tags.split(","))


def remove_node_tags(client, node_name, tags):
    """remove the corresponding tags to a node"""

    client.remove_node_tags(node_name, tags.split(","))

def disable_node(client, node_name, deactivation_intent, timeout=60):
    """Deactivate a Service Fabric cluster node with the specified deactivation.

    :param str node_name: The name of the node
    :param str deactivation_intent: Describes the intent or reason for deactivating the node.
    """
    payload = {
        "DeactivationIntent": deactivation_intent
    }

    client.disable_node(node_name, payload, timeout=timeout)


def restart_node(client, node_name, node_instance_id=0, create_fabric_dump="False",  timeout=60): # pylint: disable=too-many-arguments
    """Restarts a Service Fabric cluster node.

    :param str node_name: The name of the node
    :param str node_instance_id: The instance ID of the target node. If instance ID is specified the
                             node is restarted only if it matches with the current instance of the
                             node. A default value of "0" would match any instance ID. The instance
                             ID can be obtained using get node query
    :param str create_fabric_dump: Specify True to create a dump of the fabric node process.
                                    This is case sensitive. Default: False
    """
    payload = {
        "CreateFabricDump": create_fabric_dump,
        "NodeInstanceId": node_instance_id
    }

    client.restart_node(node_name, payload, timeout=timeout)

def add_configuration_parameter_overrides(client, config_parameter_override_list, node_name, force=False, timeout=60): # pylint: disable=too-many-arguments
    """Adds the list of configuration overrides on the specified node.

    This api allows adding all existing configuration overrides on the specified node.

    :param node_name: The name of the node.
    :type node_name: str
    :param config_parameter_override_list: Description for adding list of configuration overrides.
    :type config_parameter_override_list: list[JSON]
    :param force: Force adding configuration overrides on specified nodes. Default value is None.
    :paramtype force: bool
    """

    return client.add_configuration_parameter_overrides(node_name, config_parameter_override_list,
                                                        force=force, timeout=timeout)

def get_node_health(client, node_name, events_health_state_filter=0, timeout=60):
    """Gets the health of a Service Fabric node.

    Gets the health of a Service Fabric node. Use EventsHealthStateFilter to filter the collection
    of health events reported on the node based on the health state. If the node that you specify
    by name does not exist in the health store, this returns an error.

    :param node_name: The name of the node.
    :type node_name: str
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
    return client.get_node_health(node_name, events_health_state_filter=events_health_state_filter, timeout=timeout)


def get_node_info_list(client, continuation_token=None, max_results=0, node_status_filter="default", timeout=60): # pylint: disable=too-many-arguments
    """Gets the list of nodes in the Service Fabric cluster.

    The response includes the name, status, ID, health, uptime, and other details about the nodes.

    :param continuation_token: The continuation token parameter is used to obtain next
        set of results. A continuation token with a non-empty value is included in the response of the
        API when the results from the system do not fit in a single response. When this value is passed
        to the next API call, the API returns next set of results. If there are no further results,
        then the continuation token does not contain a value. The value of this parameter should not be
        URL encoded. Default value is None.
    :paramtype continuation_token: str
    :param node_status_filter: Allows filtering the nodes based on the NodeStatus. Only the nodes
        that are matching the specified filter value will be returned. The filter value can be one of
        the following. Known values are: "default", "all", "up", "down", "enabling", "disabling",
        "disabled", "unknown", and "removed". Default value is "default".
    :paramtype node_status_filter: str
    :param max_results: The maximum number of results to be returned as part of the paged
        queries. This parameter defines the upper bound on the number of results returned. The results
        returned can be less than the specified maximum results if they do not fit in the message as
        per the max message size restrictions defined in the configuration. If this parameter is zero
        or not specified, the paged query includes as many results as possible that fit in the return
        message. Default value is 0.
        """
    return client.get_node_info_list(continuation_token_parameter=continuation_token,
                                    node_status_filter=node_status_filter,
                                    max_results=max_results, timeout=timeout)


def start_node_transition(client, node_name, node_instance_id, node_transition_type, operation_id, # pylint: disable=too-many-arguments
                          stop_duration_in_seconds, timeout=60):
    """Starts or stops a cluster node.

        Starts or stops a cluster node.  A cluster node is a process, not the OS instance itself.  To
        start a node, pass in "Start" for the NodeTransitionType parameter.
        To stop a node, pass in "Stop" for the NodeTransitionType parameter.  This API starts the
        operation - when the API returns the node may not have finished transitioning yet.
        Call GetNodeTransitionProgress with the same OperationId to get the progress of the operation.

        :param node_name: The name of the node.
        :type node_name: str
        :param operation_id: A GUID that identifies a call of this API.  This is passed into the
            corresponding GetProgress API.
        :paramtype operation_id: str
        :param node_transition_type: Indicates the type of transition to perform.
            NodeTransitionType.Start will start a stopped node.  NodeTransitionType.Stop will stop a node
            that is up. Known values are: "Invalid", "Start", and "Stop".
        :paramtype node_transition_type: str
        :param node_instance_id: The node instance ID of the target node.  This can be determined
            through GetNodeInfo API.
        :paramtype node_instance_id: str
        :param stop_duration_in_seconds: The duration, in seconds, to keep the node stopped.  The
            minimum value is 600, the maximum is 14400.  After this time expires, the node will
            automatically come back up.
        :paramtype stop_duration_in_seconds: int
        """
    return client.start_node_transition(node_name, node_instance_id=node_instance_id,
                                        node_transition_type=node_transition_type,
                                        operation_id=operation_id,
                                        stop_duration_in_seconds=stop_duration_in_seconds,
                                        timeout=timeout)


def get_node_transition_progress(client, node_name, operation_id, timeout=60):
    """Gets the progress of an operation started using StartNodeTransition.

    Gets the progress of an operation started with StartNodeTransition using the provided
    OperationId.

    :param node_name: The name of the node.
    :type node_name: str
    :param operation_id: A GUID that identifies a call of this API.  This is passed into the
    corresponding GetProgress API.
    :paramtype operation_id: str
    """
    return client.get_node_transition_progress(node_name, operation_id=operation_id, timeout=timeout)
