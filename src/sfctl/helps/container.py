# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Help documentation for Service Fabric container commands."""

from knack.help_files import helps

helps['container invoke-api'] = """
    type: command
    short-summary: Invoke container API on a container deployed on a Service Fabric node
        for the given code package.
    parameters:
        - name: --node-name
          type: string
          short-summary: The name of the node
        - name: --application-id
          type: string
          short-summary: The identity of the application.
          long-summary: This is typically the full name of the application without the 
            'fabric:' URI scheme. Starting from version 6.0, hierarchical names are delimited 
            with the "~" character. For example, if the application name is "fabric:/myapp/app1", 
            the application identity would be "myapp~app1" in 6.0+ and 
            "myapp/app1" in previous versions.
        - name: --service-manifest-name
          type: string
          short-summary: The name of a service manifest registered as part of an 
            application type in a Service Fabric cluster.
        - name: --code-package-name
          type: string
          short-summary: The name of code package specified in service manifest registered 
            as part of an application type in a Service Fabric cluster.
        - name: --code-package-instance-id
          type: string
          short-summary: ID that uniquely identifies a code package instance deployed on a 
            service fabric node.
          long-summary: Can be retrieved by 'service code-package-list'
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
    short-summary: Gets the container logs for container deployed on a Service Fabric
        node.
    parameters:
        - name: --node-name
          type: string
          short-summary: The name of the node
        - name: --application-id
          type: string
          short-summary: The identity of the application.
          long-summary: This is typically the full name of the application without the 'fabric:' URI scheme.
             Starting from version 6.0, hierarchical names are delimited with the
             "~" character.
             For example, if the application name is "fabric:/myapp/app1", the
             application identity would be "myapp~app1" in 6.0+ and "myapp/app1" in
             previous versions.
        - name: --service-manifest-name
          type: string
          short-summary: The name of a service manifest registered as part of an application 
            type in a Service Fabric cluster.
        - name: --code-package-name
          type: string
          short-summary: The name of code package specified in service manifest registered 
            as part of an application type in a Service Fabric cluster.
        - name: --code-package-instance-id
          type: string
          short-summary: code package instance ID, which can be retrieved by 'service code-package-list'
        - name: --tail
          type: string
          short-summary: Number of lines to show from the end of the logs. 
            Default is 100. 'all' to show the complete logs.
"""
