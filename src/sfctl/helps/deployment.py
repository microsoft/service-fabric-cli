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
        - name: --input-yaml-file-paths
          type: string
          short-summary: Comma separated file paths of all the yaml files or the directory (recursive) which contain yaml files
        - name: --parameters
          type: string
          short-summary: A json file which contains the parameters which need to be overridden
    examples:
        - name: Consolidates and deploys all the resources to cluster
          text: sfctl mesh deployment create --input-yaml-file-paths ./app.yaml,./network.yaml
        - name: Consolidates and deploys all the resources in a directory to cluster
          text: sfctl mesh deployment create --input-yaml-file-paths ./resources
"""
