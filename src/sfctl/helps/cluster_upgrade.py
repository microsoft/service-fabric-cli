# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Help documentation for Service Fabric cluster upgrade commands"""

from knack.help_files import helps

helps['cluster upgrade'] = """
    type: command
    short-summary: Start upgrading the code or configuration version of a
        Service Fabric cluster
    long-summary: Validate the supplied upgrade parameters and start upgrading the code
        or configuration version of a Service Fabric cluster if the parameters
        are valid.
    parameters:
        - name: --code-version
          type: string
          short-summary: The cluster code version
        - name: --config-version
          type: string
          short-summary: The cluster configuration version
        - name: --rolling-upgrade-mode
          type: string
          short-summary: "Possible values include: 'Invalid',
            'UnmonitoredAuto', 'UnmonitoredManual', 'Monitored'"
        - name: --replica-set-check-timeout
          type: string
          short-summary: The maximum amount of time to block processing of an upgrade domain 
            and prevent loss of availability when there are unexpected issues. 
          long-summary: When this timeout expires, processing of the upgrade domain will 
            proceed regardless of availability loss issues. 
            The timeout is reset at the start of each upgrade domain. 
            Valid values are between 0 and 42949672925 inclusive.
        - name: --force-restart
          type: bool
          short-summary: Processes are forcefully restarted during upgrade even when the 
            code version has not changed
          long-summary: The upgrade only changes configuration or data
        - name: --failure-action
          type: string
          short-summary: "Possible values include: 'Invalid', 'Rollback',
            'Manual'"
        - name: --health-check-wait
          type: string
          short-summary: The length of time to wait after completing an upgrade domain 
            before starting the health checks process.
        - name: --health-check-stable
          type: string
          short-summary: The amount of time that the application or cluster must remain healthy 
            before the upgrade proceeds to the next upgrade domain.
          long-summary: It is first interpreted as a string representing an ISO 8601 duration. 
            If that fails, then it is interpreted as a number representing the total number 
            of milliseconds.
        - name: --health-check-retry
          type: string
          short-summary: The length of time between attempts to perform health checks if 
            the application or cluster is not healthy.
        - name: --upgrade-timeout
          type: string
          short-summary: The amount of time the overall upgrade has to complete before 
            FailureAction is executed. 
          long-summary: It is first interpreted as a string representing an 
            ISO 8601 duration. If that fails, then it is interpreted as a number 
            representing the total number of milliseconds.
        - name: --upgrade-domain-timeout
          type: string
          short-summary: The amount of time each upgrade domain has to complete before 
            FailureAction is executed.
          long-summary: It is first interpreted as a string representing an 
            ISO 8601 duration. If that fails, then it is interpreted as a number 
            representing the total number of milliseconds.
        - name: --warning-as-error
          type: bool
          short-summary: Indicates whether warnings are treated with the same severity as errors
        - name: --unhealthy-nodes
          type: int
          short-summary: The maximum allowed percentage of unhealthy nodes
            before reporting an error
          long-summary: For example, to allow 10% of nodes to be unhealthy,
            this value would be 10. The percentage represents the maximum
            tolerated percentage of nodes that can be unhealthy before the
            cluster is considered in error. If the percentage is respected but
            there is at least one unhealthy node, the health is evaluated as
            Warning. The percentage is calculated by dividing the number of
            unhealthy nodes over the total number of nodes in the cluster. The
            computation rounds up to tolerate one failure on small numbers of
            nodes. In large clusters, some nodes will always be down or out for
            repairs, so this percentage should be configured to tolerate that.
        - name: --unhealthy-applications
          type: int
          short-summary: The maximum allowed percentage of unhealthy
            applications before reporting an error
          long-summary: For example, to allow 10% of applications to be
            unhealthy, this value would be 10. The percentage represents the
            maximum tolerated percentage of applications that can be unhealthy
            before the cluster is considered in error. If the percentage is
            respected but there is at least one unhealthy application, the
            health is evaluated as Warning. This is calculated by dividing the
            number of unhealthy applications over the total number of
            application instances in the cluster, excluding applications of
            application types that are included in the
            ApplicationTypeHealthPolicyMap. The computation rounds up to
            tolerate one failure on small numbers of applications.
        - name: --app-type-health-map
          type: string
          short-summary: JSON encoded dictionary of pairs of application type
            name and maximum percentage unhealthy before raising error
        - name: --delta-health-evaluation
          type: bool
          short-summary: Enables delta health evaluation rather than absolute
            health evaluation after completion of each upgrade domain
        - name: --delta-unhealthy-nodes
          type: int
          short-summary: The maximum allowed percentage of nodes health
            degradation allowed during cluster upgrades
          long-summary: The delta is measured between the state of the nodes at
            the beginning of upgrade and the state of the nodes at the time of
            the health evaluation. The check is performed after every upgrade
            domain upgrade completion to make sure the global state of the
            cluster is within tolerated limits.
        - name: --upgrade-domain-delta-unhealthy-nodes
          type: int
          short-summary: The maximum allowed percentage of upgrade domain nodes
            health degradation allowed during cluster upgrades
          long-summary: The delta is measured between the state of the
            upgrade domain nodes at the beginning of upgrade and the state of
            the upgrade domain nodes at the time of the health evaluation. The
            check is performed after every upgrade domain upgrade completion
            for all completed upgrade domains to make sure the state of the
            upgrade domains is within tolerated limits.
        - name: --app-health-map
          type: string
          short-summary: JSON encoded dictionary of pairs of application name
            and maximum percentage unhealthy before raising error
"""

helps['sa-cluster config-upgrade'] = """
    type: command
    short-summary: Start upgrading the configuration of a Service Fabric
        standalone cluster
    long-summary: 
        Validate the supplied configuration upgrade parameters and start
        upgrading the cluster configuration if the parameters are valid.
    parameters:
        - name: --cluster-config
          type: string
          short-summary: The cluster configuration.
        - name: --health-check-retry
          type: string
          short-summary: The length of time between attempts to perform health checks if 
            the application or cluster is not healthy.
        - name: --health-check-wait
          type: string
          short-summary: The length of time to wait after completing an upgrade domain 
            before starting the health checks process.
        - name: --health-check-stable
          type: string
          short-summary: The amount of time that the application or cluster must remain healthy 
            before the upgrade proceeds to the next upgrade domain.
          long-summary: It is first interpreted as a string representing an ISO 8601 duration. 
            If that fails, then it is interpreted as a number representing the total number 
            of milliseconds.
        - name: --upgrade-domain-timeout
          type: string
          short-summary: The amount of time each upgrade domain has to complete before 
            FailureAction is executed.
          long-summary: It is first interpreted as a string representing an 
            ISO 8601 duration. If that fails, then it is interpreted as a number 
            representing the total number of milliseconds.
        - name: --upgrade-timeout
          type: string
          short-summary: The amount of time the overall upgrade has to complete before 
            FailureAction is executed. 
          long-summary: It is first interpreted as a string representing an 
            ISO 8601 duration. If that fails, then it is interpreted as a number 
            representing the total number of milliseconds.
        - name: --unhealthy-applications
          type: int
          short-summary: The maximum allowed percentage of unhealthy
            applications during the upgrade. Allowed values are integer values
            from zero to 100.
        - name: --unhealthy-nodes
          type: int
          short-summary: The maximum allowed percentage of unhealthy nodes
            during the upgrade. Allowed values are integer values from zero
            to 100.
        - name: --delta-unhealthy-nodes
          type: int
          short-summary: The maximum allowed percentage of delta health
            degradation during the upgrade. Allowed values are integer values
            from zero to 100.
        - name: --upgrade-domain-delta-unhealthy-nodes
          type: int
          short-summary: The maximum allowed percentage of upgrade domain delta
            health degradation during the upgrade. Allowed values are integer
            values from zero to 100.
        - name: --application-health-policies
          type: string
          short-summary: JSON encoded dictionary of pairs of application type
            name and maximum percentage unhealthy before raising error
    examples:
        - name: Start a cluster configuration update
          text: sfctl sa-cluster config-upgrade --cluster-config <YOUR CLUSTER CONFIG> --application-health-policies "{\"fabric:/System\":{\"ConsiderWarningAsError\":true}}"
"""

helps['cluster upgrade-update'] = """
    type: command
    short-summary: Update the upgrade parameters of a Service Fabric cluster
        upgrade
    parameters:
        - name: --upgrade-kind
          type: string
          short-summary: "Possible values include: 'Invalid', 'Rolling',
            'Rolling_ForceRestart'"
        - name: --rolling-upgrade-mode
          type: string
          short-summary: "Possible values include: 'Invalid',
            'UnmonitoredAuto', 'UnmonitoredManual', 'Monitored'"
        - name: --replica-set-check-timeout
          type: string
          short-summary: The maximum amount of time to block processing of an upgrade domain 
            and prevent loss of availability when there are unexpected issues. 
          long-summary: When this timeout expires, processing of the upgrade domain will 
            proceed regardless of availability loss issues. 
            The timeout is reset at the start of each upgrade domain. 
            Valid values are between 0 and 42949672925 inclusive.
        - name: --force-restart
          type: bool
          short-summary: Processes are forcefully restarted during upgrade even when the 
            code version has not changed
          long-summary: The upgrade only changes configuration or data
        - name: --failure-action
          type: string
          short-summary: "Possible values include: 'Invalid', 'Rollback',
            'Manual'"
        - name: --health-check-wait
          type: string
          short-summary: The length of time to wait after completing an upgrade domain 
            before starting the health checks process.
        - name: --health-check-stable
          type: string
          short-summary: The amount of time that the application or cluster must remain healthy 
            before the upgrade proceeds to the next upgrade domain.
          long-summary: It is first interpreted as a string representing an ISO 8601 duration. 
            If that fails, then it is interpreted as a number representing the total number 
            of milliseconds.
        - name: --health-check-retry
          type: string
          short-summary: The length of time between attempts to perform health checks if 
            the application or cluster is not healthy.
        - name: --upgrade-timeout
          type: string
          short-summary: The amount of time the overall upgrade has to complete before 
            FailureAction is executed. 
          long-summary: It is first interpreted as a string representing an 
            ISO 8601 duration. If that fails, then it is interpreted as a number 
            representing the total number of milliseconds.
        - name: --upgrade-domain-timeout
          type: string
          short-summary: The amount of time each upgrade domain has to complete before 
            FailureAction is executed.
          long-summary: It is first interpreted as a string representing an 
            ISO 8601 duration. If that fails, then it is interpreted as a number 
            representing the total number of milliseconds.
        - name: --warning-as-error
          type: bool
          short-summary: Indicates whether warnings are treated with the same severity as errors
        - name: --unhealthy-nodes
          type: int
          short-summary: The maximum allowed percentage of unhealthy nodes
            before reporting an error
          long-summary: For example, to allow 10% of nodes to be unhealthy,
            this value would be 10. The percentage represents the maximum
            tolerated percentage of nodes that can be unhealthy before the
            cluster is considered in error. If the percentage is respected but
            there is at least one unhealthy node, the health is evaluated as
            Warning. The percentage is calculated by dividing the number of
            unhealthy nodes over the total number of nodes in the cluster. The
            computation rounds up to tolerate one failure on small numbers of
            nodes. In large clusters, some nodes will always be down or out for
            repairs, so this percentage should be configured to tolerate that.
        - name: --unhealthy-applications
          type: int
          short-summary: The maximum allowed percentage of unhealthy
            applications before reporting an error
          long-summary: For example, to allow 10% of applications to be
            unhealthy, this value would be 10. The percentage represents the
            maximum tolerated percentage of applications that can be unhealthy
            before the cluster is considered in error. If the percentage is
            respected but there is at least one unhealthy application, the
            health is evaluated as Warning. This is calculated by dividing the
            number of unhealthy applications over the total number of
            application instances in the cluster, excluding applications of
            application types that are included in the
            ApplicationTypeHealthPolicyMap. The computation rounds up to
            tolerate one failure on small numbers of applications.
        - name: --app-type-health-map
          type: string
          short-summary: JSON encoded dictionary of pairs of application type
            name and maximum percentage unhealthy before raising error
        - name: --delta-health-evaluation
          type: bool
          short-summary: Enables delta health evaluation rather than absolute
            health evaluation after completion of each upgrade domain
        - name: --delta-unhealthy-nodes
          type: int
          short-summary: The maximum allowed percentage of nodes health
            degradation allowed during cluster upgrades
          long-summary: The delta is measured between the state of the nodes at
            the beginning of upgrade and the state of the nodes at the time of
            the health evaluation. The check is performed after every upgrade
            domain upgrade completion to make sure the global state of the
            cluster is within tolerated limits.
        - name: --upgrade-domain-delta-unhealthy-nodes
          type: int
          short-summary: The maximum allowed percentage of upgrade domain nodes
            health degradation allowed during cluster upgrades
          long-summary: The delta is measured between the state of the
            upgrade domain nodes at the beginning of upgrade and the state of
            the upgrade domain nodes at the time of the health evaluation. The
            check is performed after every upgrade domain upgrade completion
            for all completed upgrade domains to make sure the state of the
            upgrade domains is within tolerated limits.
        - name: --app-health-map
          type: string
          short-summary: JSON encoded dictionary of pairs of application name
            and maximum percentage unhealthy before raising error
"""
