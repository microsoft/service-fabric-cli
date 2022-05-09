# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Custom commands for the Service Fabric chaos service"""

def parse_chaos_parameters(chaos_parameters): #pylint: disable=too-many-locals
    """Parse ChaosParameters from string"""
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
        context = {"Map": chaos_context.get("Map")}

    chaos_target_filter = chaos_parameters.get("ChaosTargetFilter")
    target_filter = None
    if chaos_target_filter is not None:
        target_filter = {
            "NodeTypeInclusionList": chaos_target_filter.get("NodeTypeInclusionList"),
            "ApplicationInclusionList": chaos_target_filter.get("ApplicationTypeInclusionList")
        }

    return {"TimeToRunInSeconds": time_to_run,
            "MaxClusterStabilizationTimeoutInSeconds": max_cluster_stabilization,
            "MaxConcurrentFaults": max_concurrent_faults,
            "EnableMoveReplicaFaults": enable_move_replica_faults,
            "WaitTimeBetweenFaultsInSeconds": wait_time_between_faults,
            "WaitTimeBetweenIterationsInSeconds": wait_time_between_iterations,
            "ClusterHealthPolicy": health_policy,
            "Context": context,
            "ChaosTargetFilter": target_filter}


def parse_chaos_context(formatted_chaos_context):
    """"Parse a chaos context from a formatted context"""

    if formatted_chaos_context is None:
        return None

    return {"Map": formatted_chaos_context}

def parse_chaos_target_filter(formatted_chaos_target_filter):
    """"Parse a chaos target filter from a formatted filter"""

    if formatted_chaos_target_filter is None:
        return None

    nodetype_inclusion_list = formatted_chaos_target_filter.get('NodeTypeInclusionList', None)  # pylint: disable=line-too-long
    application_inclusion_list = formatted_chaos_target_filter.get('ApplicationInclusionList', None)  # pylint: disable=line-too-long

    return {"NodeTypeInclusionList": nodetype_inclusion_list,
            "ApplicationInclusionList": application_inclusion_list}


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

    from sfctl.custom_health import parse_app_health_map

    context = parse_chaos_context(context)

    health_map = parse_app_health_map(app_type_health_policy_map)

    health_policy = {
        "ConsiderWarningAsError": warning_as_error,
        "MaxPercentUnhealthyNodes": max_percent_unhealthy_nodes,
        "MaxPercentUnhealthyApplications": max_percent_unhealthy_apps,
        "ApplicationTypeHealthPolicyMap": health_map}

    target_filter = parse_chaos_target_filter(chaos_target_filter)

    #pylint: disable=too-many-arguments
    chaos_params = {"TimeToRunInSeconds": time_to_run,
                    "MaxClusterStabilizationTimeoutInSeconds": max_cluster_stabilization,
                    "MaxConcurrentFaults": max_concurrent_faults,
                    "EnableMoveReplicaFaults": not disable_move_replica_faults,
                    "WaitTimeBetweenFaultsInSeconds": wait_time_between_faults,
                    "WaitTimeBetweenIterationsInSeconds": wait_time_between_iterations,
                    "ClusterHealthPolicy": health_policy,
                    "Context": context,
                    "ChaosTargetFilter": target_filter}
    #pylint: enable=too-many-arguments

    client.start_chaos(chaos_params, timeout=timeout)

def get_chaos_events(client, continuation_token=None, start_time_utc=None, end_time_utc=None, max_results=0, timeout=60):
    """Gets the next segment of the Chaos events based on the continuation token or the time range.

    To get the next segment of the Chaos events, you can specify the ContinuationToken. To get the
    start of a new segment of Chaos events, you can specify the time range
    through StartTimeUtc and EndTimeUtc. You cannot specify both the ContinuationToken and the time
    range in the same call.
    When there are more than 100 Chaos events, the Chaos events are returned in multiple segments
    where a segment contains no more than 100 Chaos events and to get the next segment you make a
    call to this API with the continuation token.

    :param continuation_token: The continuation token parameter is used to obtain next
        set of results. A continuation token with a non-empty value is included in the response of the
        API when the results from the system do not fit in a single response. When this value is passed
        to the next API call, the API returns next set of results. If there are no further results,
        then the continuation token does not contain a value. The value of this parameter should not be
        URL encoded. Default value is None.
    :paramtype continuation_token_parameter: str
    :param start_time_utc: The Windows file time representing the start time of the time range
        for which a Chaos report is to be generated. Consult `DateTime.ToFileTimeUtc Method
        <https://msdn.microsoft.com/library/system.datetime.tofiletimeutc(v=vs.110>`_.aspx) for
        details. Default value is None.
    :paramtype start_time_utc: str
    :param end_time_utc: The Windows file time representing the end time of the time range for
        which a Chaos report is to be generated. Consult `DateTime.ToFileTimeUtc Method
        <https://msdn.microsoft.com/library/system.datetime.tofiletimeutc(v=vs.110>`_.aspx) for
        details. Default value is None.
    :paramtype end_time_utc: str
    :param max_results: The maximum number of results to be returned as part of the paged
        queries. This parameter defines the upper bound on the number of results returned. The results
        returned can be less than the specified maximum results if they do not fit in the message as
        per the max message size restrictions defined in the configuration. If this parameter is zero
        or not specified, the paged query includes as many results as possible that fit in the return
        message. Default value is 0.
    :paramtype max_results: long
    """

    return client.get_chaos_events(continuation_token_parameter=continuation_token, start_time_utc=start_time_utc,
                            end_time_utc=end_time_utc, max_results=max_results, timeout=timeout)
