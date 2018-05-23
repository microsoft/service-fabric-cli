# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Help documentation for Service Fabric application and compose commands."""

from knack.help_files import helps

# If the parameter name doesn't match the actual parameter name,
# no information will be provided in the help page

# To keep newlines in the help documentation, follow this format:
# long-summary: |
#    Following are the ...
#    1. text
#    2. text

helps['compose create'] = """
    type: command
    short-summary: Creates a Service Fabric application from a Compose file
    parameters:
        - name: --repo-pass
          type: string
          short-summary: Encrypted contain repository password
"""

helps['application upload'] = """
    type: command
    short-summary: Copy a Service Fabric application package to the image store
    long-summary: Optionally display upload progress for each file in the
      package. Upload progress is sent to `stderr`
    parameters:
        - name: --path
          type: string
          short-summary: Path to local application package
        - name: --show-progress
          type: bool
          short-summary: Show file upload progress for large packages
        - name: --imagestore-string
          type: string
          short-summary: Destination image store to upload the application
            package to
"""

helps['application upgrade'] = """
    type: command
    short-summary: Starts upgrading an application in the Service Fabric
      cluster
    long-summary: Validates the supplied application upgrade parameters and
      starts upgrading the application if the parameters are valid. Note
      that upgrade description replaces the existing application description.
      This means that if the parameters are not specified, the existing
      parameters on the applications will be overwritten with the empty
      parameters list. This would results in application using the default
      value of the parameters from the application manifest.
    parameters:
        - name: --application-id
          type: string
          short-summary: The identity of the application.
          long-summary: "This is typically the full name of the application
            without the 'fabric:' URI scheme. Starting from version 6.0,
            hierarchical names are delimited with the '~' character. For
            example, if the application name is 'fabric:/myapp/app1', the
            application identity would be 'myapp~app1' in 6.0+ and 'myapp/app1'
            in previous versions."
        - name: --application-version
          type: string
          short-summary: Target application version
        - name: --parameters
          type: string
          short-summary: A JSON encoded list of application parameter overrides
            to be applied when upgrading the application
        - name: --mode
          type: string
          short-summary: The mode used to monitor health during a rolling
            upgrade
        - name: --replica-set-check-timeout
          type: int
          short-summary: The maximum amount of time to block processing of an
            upgrade domain and prevent loss of availability when there are
            unexpected issues. Measured in seconds.
        - name: --force-restart
          type: bool
          short-summary: Forcefully restart processes during upgrade even
            when the code version has not changed
        - name: --failure-action
          type: string
          short-summary: The action to perform when a Monitored upgrade
            encounters monitoring policy or health policy violations
        - name: --health-check-wait-duration
          type: string
          short-summary: The amount of time to wait after completing an upgrade
            domain before applying health policies. Measured in milliseconds.
        - name: --health-check-stable-duration
          type: string
          short-summary: The amount of time that the application or cluster
            must remain healthy before the upgrade proceeds to the next
            upgrade domain. Measured in milliseconds.
        - name: --health-check-retry-timeout
          type: string
          short-summary: The amount of time to retry health evaluations when
            the application or cluster is unhealthy before the failure action
            is executed. Measured in milliseconds.
        - name: --upgrade-timeout
          type: string
          short-summary: The amount of time the overall upgrade has to complete
            before FailureAction is executed. Measured in milliseconds.
        - name: --upgrade-domain-timeout
          type: string
          short-summary: The amount of time each upgrade domain has to complete
            before FailureAction is executed. Measured in milliseconds.
        - name: --warning-as-error
          type: bool
          short-summary: Treat health evaluation warnings with the same
            severity as errors
        - name: --max-unhealthy-apps
          type: int
          short-summary: The maximum allowed percentage of unhealthy deployed
            applications. Represented as a number between 0 and 100.
        - name: --default-service-health-policy
          type: string
          short-summary: JSON encoded specification of the health policy used
            by default to evaluate the health of a service type
        - name: --service-health-policy
          type: string
          short-summary: JSON encoded map with service type health
            policy per service type name. The map is empty be default.
"""
