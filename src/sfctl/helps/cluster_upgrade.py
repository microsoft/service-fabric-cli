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
    long-summary: Validate the supplied upgrade parameters and start upgrading
        the code or configuration version of a Service Fabric cluster if the
        parameters are valid.
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
          short-summary: Upgrade replica set check timeout measured in
            seconds
        - name: --force-restart
          type: bool
          short-summary: Force restart
        - name: --failure-action
          type: string
          short-summary: "Possible values include: 'Invalid', 'Rollback',
            'Manual'"
        - name: --health-check-wait
          type: string
          short-summary: Health check wait duration measured in milliseconds
        - name: --health-check-stable
          type: string
          short-summary: Health check stable duration measured in milliseconds
        - name: --health-check-retry
          type: string
          short-summary: Health check retry timeout measured in milliseconds
        - name: --upgrade-timeout
          type: string
          short-summary: Upgrade timeout measured in milliseconds
        - name: --upgrade-domain-timeout
          type: string
          short-summary: Upgrade domain timeout measured in milliseconds
        - name: --warning-as-error
          type: bool
          short-summary: Warnings are treated with the same severity as errors
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
    long-summary: Validate the supplied configuration upgrade parameters and
        start upgrading the cluster configuration if the parameters are valid.
    parameters:
        - name: --cluster-config
          type: string
          short-summary: The cluster configuration
        - name: --health-check-retry
          type: string
          short-summary: The length of time between attempts to perform a
            health checks if the application or cluster is not healthy
        - name: --health-check-wait
          type: string
          short-summary: The length of time to wait after completing an
            upgrade domain before starting the health checks process
        - name: --health-check-stable
          type: string
          short-summary: The length of time that the application or cluster
            must remain healthy
        - name: --upgrade-domain-timeout
          type: string
          short-summary: The timeout for the upgrade domain
        - name: --upgrade-timeout
          type: string
          short-summary: The upgrade timeout
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
          short-summary: Upgrade replica set check timeout measured in
            seconds
        - name: --force-restart
          type: bool
          short-summary: Force restart
        - name: --failure-action
          type: string
          short-summary: "Possible values include: 'Invalid', 'Rollback',
            'Manual'"
        - name: --health-check-wait
          type: string
          short-summary: Health check wait duration measured in milliseconds
        - name: --health-check-stable
          type: string
          short-summary: Health check stable duration measured in milliseconds
        - name: --health-check-retry
          type: string
          short-summary: Health check retry timeout measured in milliseconds
        - name: --upgrade-timeout
          type: string
          short-summary: Upgrade timeout measured in milliseconds
        - name: --upgrade-domain-timeout
          type: string
          short-summary: Upgrade domain timeout measured in milliseconds
        - name: --warning-as-error
          type: bool
          short-summary: Warnings are treated with the same severity as errors
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