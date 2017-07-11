"""Custom commands for managing the Service Fabric chaos test service."""

def sf_start_chaos(
        client, time_to_run="4294967295", max_cluster_stabilization=60,
        max_concurrent_faults=1, disable_move_replica_faults=False,
        wait_time_between_faults=20,
        wait_time_between_iterations=30, warning_as_error=False,
        max_percent_unhealthy_nodes=0,
        max_percent_unhealthy_applications=0,
        app_type_health_policy_map=None, timeout=60):
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

    :param int max_percent_unhealthy_applications: When evaluating cluster
    health during Chaos, the maximum allowed percentage of unhealthy
    applications before reporting an error.

    :param str app_type_health_policy_map: JSON encoded list with max
    intger that represents the MaxPercentUnhealthyApplications percentage
    from azure.servicefabric.models.cluster_health_policy import ClusterHealthPolicy
    """


    health_policy = ClusterHealthPolicy(warning_as_error,
                                        max_percent_unhealthy_nodes,
                                        max_percent_unhealthy_applications,
                                        health_map)
                                   not disable_move_replica_faults,
                                   wait_time_between_faults,
                                   wait_time_between_iterations,
                                   health_policy,
                                   None)

    client.start_chaos(chaos_params, timeout)
