# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Help documentation for Service Fabric Chaos commands."""

from knack.help_files import helps

helps['chaos start'] = """
    type: command
    short-summary: Starts Chaos in the cluster.
    long-summary: If Chaos is not already running in the cluster,
        it starts Chaos with the passed in Chaos parameters.
        If Chaos is already running when this call is made,
        the call fails with the error code FABRIC_E_CHAOS_ALREADY_RUNNING.
    parameters:
        - name: --time-to-run
          type: string
          short-summary: Total time (in seconds) for which Chaos will run
            before automatically stopping. The maximum allowed value is 4,294,967,295
            (System.UInt32.MaxValue).
        - name: --warning-as-error
          type: bool
          short-summary: Sets the health policy to treat warning as errors.
        - name: --max-cluster-stabilization
          type: int
          short-summary: The maximum amount of time to wait
            for all cluster entities to become stable and healthy.
          long-summary: Chaos executes in iterations and at the start of
            each iteration it validates the health of cluster entities.
            During validation if a cluster entity is not stable and healthy
            within MaxClusterStabilizationTimeoutInSeconds,
            Chaos generates a validation failed event.
        - name: --max-concurrent-faults
          type: int
          short-summary: The maximum number of concurrent faults induced
            per iteration. Chaos executes in iterations and two consecutive
            iterations are separated by a validation phase. The higher
            the concurrency, the more aggressive the injection of
            faults -- inducing more complex series of states to uncover bugs.
            The recommendation is to start with a value of 2 or 3 and to
            exercise caution while moving up.
        - name: --disable-move-replica-faults
          type: bool
          short-summary: Disables the move primary and move secondary faults.
        - name: --wait-time-between-faults
          type: int
          short-summary: Wait time (in seconds) between consecutive faults
            within a single iteration.
          long-summary: The larger the value, the lower the overlapping
            between faults and the simpler the sequence of state transitions
            that the cluster goes through. The recommendation is to start
            with a value between 1 and 5 and exercise caution while moving up.
        - name: --wait-time-between-iterations
          type: int
          short-summary: Time-separation (in seconds) between two consecutive
            iterations of Chaos. The larger the value, the lower the fault
            injection rate.
        - name: --max-percent-unhealthy-nodes
          type: int
          short-summary: When evaluating cluster health during Chaos, the
            maximum allowed percentage of unhealthy nodes before
            reporting an error.
          long-summary: The maximum allowed percentage of unhealthy nodes
            before reporting an error. For example, to allow 10% of nodes
            to be unhealthy, this value would be 10. The percentage represents
            the maximum tolerated percentage of nodes that can be unhealthy
            before the cluster is considered in error. If the percentage is
            respected but there is at least one unhealthy node, the health
            is evaluated as Warning. The percentage is calculated by dividing
            the number of unhealthy nodes over the total number of nodes
            in the cluster. The computation rounds up to tolerate one failure
            on small numbers of nodes. Default percentage is zero.
            In large clusters, some nodes will always be down or out for
            repairs, so this percentage should be configured to tolerate that.
        - name: --max-percent-unhealthy-apps
          type: int
          short-summary: When evaluating cluster health during Chaos,
            the maximum allowed percentage of unhealthy applications
            before reporting an error.
          long-summary: The maximum allowed percentage of unhealthy
            applications before reporting an error. For example,
            to allow 10% of applications to be unhealthy, this value would be 10.
            The percentage represents the maximum tolerated percentage
            of applications that can be unhealthy before the cluster is
            considered in error. If the percentage is respected but
            there is at least one unhealthy application, the health
            is evaluated as Warning. This is calculated by dividing
            the number of unhealthy applications over the total number
            of application instances in the cluster, excluding applications
            of application types that are included in the
            ApplicationTypeHealthPolicyMap. The computation rounds up
            to tolerate one failure on small numbers of applications.
            Default percentage is zero.
        - name: --app-type-health-policy-map
          type: string
          short-summary: JSON encoded list with max
            percentage unhealthy applications for specific application
            types. Each entry specifies as a key the application type
            name and as  a value an integer that represents the
            MaxPercentUnhealthyApplications percentage used to evaluate
            the applications of the specified application type.
          long-summary: Defines a map with max percentage unhealthy
            applications for specific application types. Each entry
            specifies as key the application type name and as value
            an integer that represents the MaxPercentUnhealthyApplications
            percentage used to evaluate the applications of the specified
            application type. The application type health policy map
            can be used during cluster health evaluation to describe
            special application types. The application types included
            in the map are evaluated against the percentage specified
            in the map, and not with the global MaxPercentUnhealthyApplications
            defined in the cluster health policy. The applications of
            application types specified in the map are not counted against
            the global pool of applications. For example, if some
            applications of a type are critical, the cluster administrator
            can add an entry to the map for that application type and assign
            it a value of 0% (that is, do not tolerate any failures).
            All other applications can be evaluated with
            MaxPercentUnhealthyApplications set to 20% to tolerate
            some failures out of the thousands of application instances.
            The application type health policy map is used only if the
            cluster manifest enables application type health evaluation
            using the configuration entry for
            HealthManager/EnableApplicationTypeHealthEvaluation.
        - name: --context
          type: string
          short-summary: JSON encoded map of (string, string) type key-value
            pairs. The map can be used to record information about the Chaos
            run. There cannot be more than 100 such pairs and each
            string (key or value) can be at most 4095 characters long.
            This map is set by the starter of the Chaos run to optionally
            store the context about the specific run.
        - name: --chaos-target-filter
          type: string
          short-summary: JSON encoded dictionary with two
            string type keys. The two keys are NodeTypeInclusionList and
            ApplicationInclusionList. Values for both of these keys are list of
            string. chaos_target_filter defines all filters for targeted
            Chaos faults, for example, faulting only certain node types or
            faulting only certain applications.
          long-summary: If chaos_target_filter is not used, Chaos faults all cluster entities.
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
            All types of faults (restart node, restart code package, remove replica,
            restart replica, move primary, and move secondary) are enabled for
            the nodes of these node types.
            If a node type (say NodeTypeX) does not appear in the
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
            up on a node of a node type that is included in NodeTypeInclusionList.
            However if applicationX is tied to nodeTypeY through placement
            constraints and applicationX is absent from ApplicationInclusionList
            and nodeTypeY is absent from NodeTypeInclusionList, then
            applicationX will never be faulted. At most 1000 application
            names can be included in this list, to increase this number,
            a config upgrade is required for
            MaxNumberOfApplicationsInChaosEntityFilter configuration.
"""

helps['chaos schedule set'] = """
    type: command
    short-summary: Set the Chaos Schedule to be used by Chaos.
    long-summary: Set the Chaos Schedule currently in use by Chaos. Chaos will
        automatically schedule runs based on the Chaos Schedule.
        The version in the provided input schedule must match the version of
        the Chaos Schedule on the server.
        If the version provided does not match the version on the server, the
        Chaos Schedule is not updated.
        If the version provided matches the version on the server, then the
        Chaos Schedule is updated and the version of the Chaos Schedule on the
        server is incremented up by one and wraps back to 0 after 2,147,483,647.


        If Chaos is running when this call is made, the call will fail.


        Example

        The following command sets a schedule (assuming the current schedule has version 0) that starts on 2016-01-01 and expires on 2038-01-01 that runs Chaos 24 hours of the day, 7 days a week.


        sfctl chaos schedule set --version 0 --start-date-utc "2016-01-01T00:00:00.000Z" --expiry-date-utc "2038-01-01T00:00:00.000Z" --chaos-parameters-dictionary [{\\\"Key\\\":\\\"adhoc\\\",\\\"Value\\\":{\\\"MaxConcurrentFaults\\\":3,\\\"EnableMoveReplicaFaults\\\":true,\\\"ChaosTargetFilter\\\":{\\\"NodeTypeInclusionList\\\":[\\\"N0010Ref\\\",\\\"N0020Ref\\\",\\\"N0030Ref\\\",\\\"N0040Ref\\\",\\\"N0050Ref\\\"]},\\\"MaxClusterStabilizationTimeoutInSeconds\\\":60,\\\"WaitTimeBetweenIterationsInSeconds\\\":15,\\\"WaitTimeBetweenFaultsInSeconds\\\":30,\\\"TimeToRunInSeconds\\\":\\\"600\\\",\\\"Context\\\":{\\\"Map\\\":{\\\"test\\\":\\\"value\\\"}},\\\"ClusterHealthPolicy\\\":{\\\"MaxPercentUnhealthyNodes\\\":0,\\\"ConsiderWarningAsError\\\":true,\\\"MaxPercentUnhealthyApplications\\\":0}}}] --jobs [{\\\"ChaosParameters\\\":\\\"adhoc\\\",\\\"Days\\\":{\\\"Sunday\\\":true,\\\"Monday\\\":true,\\\"Tuesday\\\":true,\\\"Wednesday\\\":true,\\\"Thursday\\\":true,\\\"Friday\\\":true,\\\"Saturday\\\":true},\\\"Times\\\":[{\\\"StartTime\\\":{\\\"Hour\\\":0,\\\"Minute\\\":0},\\\"EndTime\\\":{\\\"Hour\\\":23,\\\"Minute\\\":59}}]}]


        Chaos will now be scheduled on the cluster.

    parameters:
        - name: --version
          type: int
          short-summary: The version number of the Schedule.
        - name: --start-date-utc
          type: string
          short-summary: The date and time for when to start using the Schedule to schedule Chaos.
        - name: --expiry-date-utc
          type: string
          short-summary: The date and time for when to stop using the Schedule to schedule Chaos.
        - name: --chaos-parameters-dictionary
          type: string
          short-summary: JSON encoded list representing a mapping of string names to
            ChaosParameters to be used by Jobs.
        - name: --jobs
          type: string
          short-summary: JSON encoded list of ChaosScheduleJobs representing when to run Chaos and
            with what parameters to run Chaos with.
"""