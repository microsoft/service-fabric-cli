# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Help documentation for managing Service Fabric Mesh Resources."""

from knack.help_files import helps

helps['mesh deployment create'] = """
    type: command
    short-summary: Creates a deployment of Service Fabric Mesh Resources
    parameters:
        - name: --input-yaml-paths
          type: string
          short-summary: Comma separated relative/absolute file paths of all the yaml files or relative/absolute path of the directory (recursive) which contain yaml files
        - name: --parameters
          type: string
          short-summary: A relative/absolute to json file which contains the parameters that need to be overridden
    examples:
        - name: Consolidates and deploys all the resources to cluster by overriding the parameters mentioned in the param.json file
          text: sfctl mesh deployment create --input-yaml-paths ./app.yaml,./network.yaml --parameters ./param.json
        - name: Consolidates and deploys all the resources in a directory to cluster by overriding the parameters mentioned in the param.json file
          text: sfctl mesh deployment create --input-yaml-paths ./resources --parameters ./param.json
"""
