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
    max_cluster_stabilization = chaos_parameters.get("MaxClusterStabilizationTimeoutInSeconds")
    max_concurrent_faults = chaos_parameters.get("MaxConcurrentFaults")
    enable_move_replica_faults = chaos_parameters.get("EnableMoveReplicaFaults")
    wait_time_between_faults = chaos_parameters.get("WaitTimeBetweenFaultsInSeconds")
    wait_time_between_iterations = chaos_parameters.get("WaitTimeBetweenIterationsInSeconds")

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
        context = ChaosContext(map=chaos_context.get("Map"))

    chaos_target_filter = chaos_parameters.get("ChaosTargetFilter")
    target_filter = None
    if chaos_target_filter is not None:
        target_filter = ChaosTargetFilter(
            node_type_inclusion_list=chaos_target_filter.get("NodeTypeInclusionList"),
            application_inclusion_list=chaos_target_filter.get("ApplicationTypeInclusionList"))

    return ChaosParameters(time_to_run_in_seconds=time_to_run,
                           max_cluster_stabilization_timeout_in_seconds=max_cluster_stabilization,
                           max_concurrent_faults=max_concurrent_faults,
                           enable_move_replica_faults=enable_move_replica_faults,
                           wait_time_between_faults_in_seconds=wait_time_between_faults,
                           wait_time_between_iterations_in_seconds=wait_time_between_iterations,
                           cluster_health_policy=health_policy,
                           context=context,
                           chaos_target_filter=target_filter)

def parse_chaos_context(formatted_chaos_context):
    """"Parse a chaos context from a formatted context"""
    from azure.servicefabric.models.chaos_context import (
        ChaosContext
    )

    if formatted_chaos_context is None:
        return None

    return ChaosContext(map=formatted_chaos_context)

def parse_chaos_target_filter(formatted_chaos_target_filter):
    """"Parse a chaos target filter from a formatted filter"""
    from azure.servicefabric.models.chaos_target_filter import (
        ChaosTargetFilter
    )

    if formatted_chaos_target_filter is None:
        return None

    nodetype_inclusion_list = formatted_chaos_target_filter.get('NodeTypeInclusionList', None) # pylint: disable=line-too-long
    application_inclusion_list = formatted_chaos_target_filter.get('ApplicationInclusionList', None) # pylint: disable=line-too-long

    return ChaosTargetFilter(node_type_inclusion_list=nodetype_inclusion_list,
                             application_inclusion_list=application_inclusion_list)

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

    from azure.servicefabric.models.chaos_parameters import (
        ChaosParameters
    )
    from azure.servicefabric.models.cluster_health_policy import (
        ClusterHealthPolicy
    )
    from sfctl.custom_health import parse_app_health_map

    context = parse_chaos_context(context)

    health_map = parse_app_health_map(app_type_health_policy_map)

    health_policy = ClusterHealthPolicy(
        consider_warning_as_error=warning_as_error,
        max_percent_unhealthy_nodes=max_percent_unhealthy_nodes,
        max_percent_unhealthy_applications=max_percent_unhealthy_apps,
        application_type_health_policy_map=health_map)

    target_filter = parse_chaos_target_filter(chaos_target_filter)

    #pylint: disable=too-many-arguments
    chaos_params = ChaosParameters(
        time_to_run_in_seconds=time_to_run,
        max_cluster_stabilization_timeout_in_seconds=max_cluster_stabilization,
        max_concurrent_faults=max_concurrent_faults,
        enable_move_replica_faults=not disable_move_replica_faults,
        wait_time_between_faults_in_seconds=wait_time_between_faults,
        wait_time_between_iterations_in_seconds=wait_time_between_iterations,
        cluster_health_policy=health_policy,
        context=context,
        chaos_target_filter=target_filter)
    #pylint: enable=too-many-arguments

    client.start_chaos(chaos_params, timeout)
