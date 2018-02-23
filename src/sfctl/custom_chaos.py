# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Custom commands for the Service Fabric chaos service"""

def parse_chaos_parameters(chaos_parameters): #pylint: disable=too-many-locals
    """Parse ChaosParameters from string"""
    from azure.servicefabric.models.chaos_parameters import (
        ChaosParameters
    )
    from azure.servicefabric.models.chaos_context import (
        ChaosContext
    )

    from azure.servicefabric.models.chaos_target_filter import (
        ChaosTargetFilter
    )

    from sfctl.custom_cluster_upgrade import create_cluster_health_policy

    time_to_run = chaos_parameters.get("TimeToRunInSeconds")
    max_cluster_stabilization = \
        chaos_parameters.get("MaxClusterStabilizationTimeoutInSeconds")
    max_concurrent_faults = chaos_parameters.get("MaxConcurrentFaults")
    enable_move_replica_faults = \
        chaos_parameters.get("EnableMoveReplicaFaults")
    wait_time_between_faults = \
        chaos_parameters.get("WaitTimeBetweenFaultsInSeconds")
    wait_time_between_iterations = \
        chaos_parameters.get("WaitTimeBetweenIterationsInSeconds")

    cluster_health_policy = chaos_parameters.get("ClusterHealthPolicy")
    health_policy = None
    if cluster_health_policy is not None:
        health_policy = create_cluster_health_policy(
            cluster_health_policy.get("ConsiderWarningAsError"),
            cluster_health_policy.get("MaxPercentUnhealthyNodes"),
            cluster_health_policy.get("MaxPercentUnhealthyApplications"),
            cluster_health_policy.get("ApplicationTypeHealthPolicyMap"))

    chaos_context = chaos_parameters.get("Context")
    context = None
    if chaos_context is not None:
        context = ChaosContext(chaos_context.get("Map"))

    chaos_target_filter = chaos_parameters.get("ChaosTargetFilter")
    target_filter = None
    if chaos_target_filter is not None:
        target_filter = ChaosTargetFilter(
            chaos_target_filter.get("NodeTypeInclusionList"),
            chaos_target_filter.get("ApplicationTypeInclusionList"))

    return ChaosParameters(time_to_run,
                           max_cluster_stabilization,
                           max_concurrent_faults,
                           enable_move_replica_faults,
                           wait_time_between_faults,
                           wait_time_between_iterations,
                           health_policy,
                           context,
                           target_filter)

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

    nodetype_inclusion_list = formatted_chaos_target_filter.get('NodeTypeInclusionList', None) # pylint: disable=line-too-long
    application_inclusion_list = formatted_chaos_target_filter.get('ApplicationInclusionList', None) # pylint: disable=line-too-long

    return ChaosTargetFilter(nodetype_inclusion_list, application_inclusion_list) # pylint: disable=line-too-long

def start(client, time_to_run="4294967295", max_cluster_stabilization=60, #pylint: disable=too-many-arguments,too-many-locals,missing-docstring
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
    entry specifies as a key the application type name and as a value an
    integer that represents the MaxPercentUnhealthyApplications percentage
    used to evaluate the applications of the specified application type.
    :param ChaosContext context: mapping of settings for Chaos
    :param ChaosTargetFilter chaos_target_filter: Specification of which nodes and
    applications to target for faults
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

    #pylint: disable=too-many-arguments
    chaos_params = ChaosParameters(time_to_run,
                                   max_cluster_stabilization,
                                   max_concurrent_faults,
                                   not disable_move_replica_faults,
                                   wait_time_between_faults,
                                   wait_time_between_iterations,
                                   health_policy,
                                   context,
                                   target_filter)
    #pylint: enable=too-many-arguments

    client.start_chaos(chaos_params, timeout)
