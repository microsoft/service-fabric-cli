# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Help documentation for Service Fabric compose deployment commands."""

from knack.help_files import helps

helps['compose create'] = """
    type: command
    short-summary: Creates a Service Fabric compose deployment
    parameters:
        - name: --deployment-name
          type: string
          short-summary: The name of the deployment
        - name: --file-path
          type: string
          short-summary: Path to the target Docker Compose file
        - name: --user
          type: string
          short-summary: User name to connect to container registry
        - name: --has-pass
          type: bool
          short-summary: Will prompt for a password to the container registry
        - name: --encrypted-pass
          type: string
          short-summary: Rather than prompting for a container registry
            password, use an already encrypted pass-phrase
"""

helps['compose upgrade'] = """
    type: command
    short-summary: Starts upgrading a compose deployment in the Service Fabric
        cluster
    long-summary: Validates the supplied upgrade parameters and starts
        upgrading the deployment if the parameters are valid
    parameters:
        - name: --deployment-name
          type: string
          short-summary: The name of the deployment
        - name: --file-path
          type: string
          short-summary: Path to the target Docker compose file
        - name: --user
          type: string
          short-summary: User name to connect to container registry
        - name: --has-pass
          type: bool
          short-summary: Will prompt for a password to the container registry
        - name: --encrypted-pass
          type: string
          short-summary: Rather than prompting for a container registry
            password, use an already encrypted pass-phrase
        - name: --upgrade-mode
          type: string
          short-summary: "Possible values include: 'Invalid',
            'UnmonitoredAuto', 'UnmonitoredManual', 'Monitored'"
        - name: --replica-set-check
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
        - name: --unhealthy-app
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
            application instances in the cluster.
        - name: --default-svc-type-health-map
          type: string
          short-summary: JSON encoded dictionary that describe the
            health policy used to evaluate the health of services
        - name: --svc-type-health-map
          type: string
          short-summary: JSON encoded list of objects that describe the
            health policies used to evaluate the health of different service
            types
"""
