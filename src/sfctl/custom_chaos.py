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
