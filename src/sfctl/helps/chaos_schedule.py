# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Help documentation for Service Fabric chaos-schedule commands"""

from knack.help_files import helps

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


        sfctl chaos-schedule set --version 0 --start-date-utc "2016-01-01T00:00:00.000Z" --expiry-date-utc "2038-01-01T00:00:00.000Z" --chaos-parameters-dictionary [{\\\"Key\\\":\\\"adhoc\\\",\\\"Value\\\":{\\\"MaxConcurrentFaults\\\":3,\\\"EnableMoveReplicaFaults\\\":true,\\\"ChaosTargetFilter\\\":{\\\"NodeTypeInclusionList\\\":[\\\"N0010Ref\\\",\\\"N0020Ref\\\",\\\"N0030Ref\\\",\\\"N0040Ref\\\",\\\"N0050Ref\\\"]},\\\"MaxClusterStabilizationTimeoutInSeconds\\\":60,\\\"WaitTimeBetweenIterationsInSeconds\\\":15,\\\"WaitTimeBetweenFaultsInSeconds\\\":30,\\\"TimeToRunInSeconds\\\":\\\"600\\\",\\\"Context\\\":{\\\"Map\\\":{\\\"test\\\":\\\"value\\\"}},\\\"ClusterHealthPolicy\\\":{\\\"MaxPercentUnhealthyNodes\\\":0,\\\"ConsiderWarningAsError\\\":true,\\\"MaxPercentUnhealthyApplications\\\":0}}}] --jobs [{\\\"ChaosParameters\\\":\\\"adhoc\\\",\\\"Days\\\":{\\\"Sunday\\\":true,\\\"Monday\\\":true,\\\"Tuesday\\\":true,\\\"Wednesday\\\":true,\\\"Thursday\\\":true,\\\"Friday\\\":true,\\\"Saturday\\\":true},\\\"Times\\\":[{\\\"StartTime\\\":{\\\"Hour\\\":0,\\\"Minute\\\":0},\\\"EndTime\\\":{\\\"Hour\\\":23,\\\"Minute\\\":59}}]}]


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
