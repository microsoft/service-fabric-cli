# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Help documentation for Service Fabric container commands."""

from knack.help_files import helps

helps['container invoke-api'] = """
    type: command
    short-summary: Invoke container REST API
    parameters:
        - name: --node-name
          type: string
          short-summary: The name of the node
        - name: --application-id
          type: string
          short-summary: application identity
        - name: --service-manifest-name
          type: string
          short-summary: service manifest name
        - name: --code-package-name
          type: string
          short-summary: code packge name
        - name: --code-package-instance-id
          type: string
          short-summary: code package instance ID, which can be retrieved by 'service code-package-list'
        - name: --container-api-uri-path
          type: string
          short-summary: container REST API URI path, use '{id}' in place of container name/id
        - name: --container-api-http-verb
          type: string
          short-summary: HTTP verb for container REST API, defaults to GET
        - name: --container-api-content-type
          type: string
          short-summary: content type for container REST API, defaults to 'application/json'
        - name: --container-api-body
          type: string
          short-summary: HTTP request body for container REST API
"""

helps['container logs'] = """
    type: command
    short-summary: Retrieving container logs
    parameters:
        - name: --node-name
          type: string
          short-summary: The name of the node
        - name: --application-id
          type: string
          short-summary: application identity
        - name: --service-manifest-name
          type: string
          short-summary: service manifest name
        - name: --code-package-name
          type: string
          short-summary: code packge name
        - name: --code-package-instance-id
          type: string
          short-summary: code package instance ID, which can be retrieved by 'service code-package-list'
        - name: --tail
          type: string
          short-summary: Only return this number of log lines from the end of the logs. Specify as an integer or all to output all log lines. Defaults to 'all'
"""
