# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Custom commands for the Service Fabric chaos service"""

def parse_chaos_context(formatted_chaos_context):
    """"Parse a chaos context from a formatted context"""
    from azure.servicefabric.models.chaos_context import (
    ChaosContext
    )

    if formatted_chaos_context is None:
        return None

    return ChaosContext(formatted_chaos_context)

def parse_chaos_target_filter(formatted_chaos_target_filter):
    """"Parse a chaos target filter from a formatted filter"""
    from azure.servicefabric.models.chaos_target_filter import (
        ChaosTargetFilter
    )

    if formatted_chaos_target_filter is None:
        return None

    nodetype_inclusion_list = formatted_chaos_target_filter.get('NodeTypeInclusionList', None)
    application_inclusion_list = formatted_chaos_target_filter.get('ApplicationInclusionList', None)

    return ChaosTargetFilter(nodetype_inclusion_list, application_inclusion_list)

def start( #pylint: disable=too-many-arguments,too-many-locals
    client, time_to_run="4294967295", max_cluster_stabilization=60,
    max_concurrent_faults=1, disable_move_replica_faults=False,
    wait_time_between_faults=20,
    wait_time_between_iterations=30,
    warning_as_error=False,
    max_percent_unhealthy_nodes=0,
    max_percent_unhealthy_apps=0,
    app_type_health_policy_map=None,
    context=None,
    chaos_target_filter=None,
    timeout=60):
    """
    If Chaos is not already running in the cluster, starts running Chaos with
    the specified in Chaos parameters.
    :param str time_to_run: Total time (in seconds) for which Chaos will run
    before automatically stopping. The maximum allowed value is 4,294,967,295
    (System.UInt32.MaxValue).
    :param int max_cluster_stabilization: The maximum amount of time to wait
    for all cluster entities to become stable and healthy.
    :param int max_concurrent_faults: The maximum number of concurrent faults
    induced per iteration.
    :param bool disable_move_replica_faults: Disables the move primary and move
    secondary faults.
    :param int wait_time_between_faults: Wait time (in seconds) between
    consecutive faults within a single iteration.
    :param int wait_time_between_iterations: Time-separation (in seconds)
    between two consecutive iterations of Chaos.
    :param bool warning_as_error: When evaluating cluster health during
    Chaos, treat warnings with the same severity as errors.
    :param int max_percent_unhealthy_nodes: When evaluating cluster health
    during Chaos, the maximum allowed percentage of unhealthy nodes before
    reporting an error.
    :param int max_percent_unhealthy_apps: When evaluating cluster
    health during Chaos, the maximum allowed percentage of unhealthy
    applications before reporting an error.
    :param str app_type_health_policy_map: JSON encoded list with max
    percentage unhealthy applications for specific application types. Each
    entry specifies as a key the application type name and as  a value an
    integer that represents the MaxPercentUnhealthyApplications percentage
    used to evaluate the applications of the specified application type.
    :param str context: JSON encoded map of (string, string) type key-value
    pairs. The map can be used to record information about the Chaos run. 
    There cannot be more than 100 such pairs 
    and each string (key or value) can be at most 4095 characters long.
    This map is set by the starter of the Chaos run to optionally
    store the context about the specific run.
    :param str chaos_target_filter: JSON encoded dictionary with two
    string type keys. The two keys are NodeTypeInclusionList and
    ApplicationInclusionList. Values for both of these keys are list of
    string. chaos_target_filter defines all filters for targeted
    Chaos faults, for example, faulting only certain node types or
    faulting only certain applications.
    If chaos_target_filter is not used, Chaos faults all cluster entities.
    If chaos_target_filter is used, Chaos faults only the entities that
    meet the chaos_target_filter specification. NodeTypeInclusionList
    and ApplicationInclusionList allow a union semantics only. It is
    not possible to specify an intersection of NodeTypeInclusionList
    and ApplicationInclusionList. For example,
    it is not possible to specify "fault this application only when
    it is on that node type." Once an entity is included in either
    NodeTypeInclusionList or ApplicationInclusionList, that entity cannot
    be excluded using ChaosTargetFilter. Even if applicationX does not 
    appear in ApplicationInclusionList, in some Chaos iteration
    applicationX can be faulted because it happens to be on a node of
    nodeTypeY that is included in NodeTypeInclusionList.
    If both NodeTypeInclusionList and ApplicationInclusionList
    are empty, an ArgumentException is thrown.
    All types of faults (restart node, restart codepackage, remove replica,
    restart replica, move primary, and move secondary) are enabled for
    the nodes of these node types.
    If a nodetype (say NodeTypeX) does not appear in the
    NodeTypeInclusionList, then node level faults (like NodeRestart)
    will never be enabled for the nodes of NodeTypeX, but code package
    and replica faults can still be enabled for NodeTypeX 
    if an application in the ApplicationInclusionList happens to
    reside on a node of NodeTypeX. 
    At most 100 node type names can be included in this list,
    to increase this number, a config upgrade is required for
    MaxNumberOfNodeTypesInChaosEntityFilter configuration.
    All replicas belonging to services of these applications are
    amenable to replica faults (restart replica, remove replica,
    move primary, and move secondary) by Chaos.
    Chaos may restart a code package only if the code package hosts
    replicas of these applications only.
    If an application does not appear in this list, it can still
    be faulted in some Chaos iteration if the application ends
    up on a node of a node type that is  incuded in NodeTypeInclusionList.
    However if applicationX is tied to nodeTypeY through placement
    constraints and applicationX is absent from ApplicationInclusionList
    and nodeTypeY is absent from NodeTypeInclusionList, then
    applicationX will never be faulted. At most 1000 application
    names can be included in this list, to increase this number,
    a config upgrade is required for 
    MaxNumberOfApplicationsInChaosEntityFilter configuration.
    """
    from azure.servicefabric.models.chaos_parameters import (
        ChaosParameters
    )
    from azure.servicefabric.models.cluster_health_policy import (
        ClusterHealthPolicy
    )
    from sfctl.custom_health import parse_app_health_map

    context = parse_chaos_context(context)

    health_map = parse_app_health_map(app_type_health_policy_map)

    health_policy = ClusterHealthPolicy(warning_as_error,
                                        max_percent_unhealthy_nodes,
                                        max_percent_unhealthy_apps,
                                        health_map)

    target_filter = parse_chaos_target_filter(chaos_target_filter)

    chaos_params = ChaosParameters(time_to_run, max_cluster_stabilization,
                                   max_concurrent_faults,
                                   not disable_move_replica_faults,
                                   wait_time_between_faults,
                                   wait_time_between_iterations,
                                   health_policy,
                                   context,
                                   target_filter)

    client.start_chaos(chaos_params, timeout)
