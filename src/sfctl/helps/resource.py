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
        - name: --yaml-files-or-directory
          type: string
          short-summary: Comma seperated file paths of all the yaml files or the directory(recursive) which contain yaml files
    examples:
        - name: Consolidates and deploys all the resources to a cluster endpoint
          text: sfctl mesh deployment create --yaml-files-or-directory ./app.yaml,./network.yaml
        - name: Consolidates and deploys all the resources in a directory to a cluster endpoint
          text: sfctl mesh deployment create --yaml-files-or-directory ./resources       
"""