# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Help documentation for Service Fabric Node tag commands."""

from knack.help_files import helps

# If the parameter name doesn't match the actual parameter name,
# no information will be provided in the help page

# To keep newlines in the help documentation, follow this format:
# long-summary: |
#    Following are the ...
#    1. text
#    2. text

helps['node add-node-tags'] = """
    type: command
    short-summary: Add a list of tags to a node.
    parameters:
        - name: --node-name
          type: string
          short-summary: The name of the node.
        - name: --tags
          type: string
          short-summary: CSV list of tags to be added, i.e tagA,tagB,tagC
"""

helps['node remove-node-tags'] = """
    type: command
    short-summary: Remove a list of tags to a node.
    parameters:
        - name: --node-name
          type: string
          short-summary: The name of the node.
        - name: --tags
          type: string
          short-summary: CSV list of tags to be removed, i.e tagA,tagB,tagC
"""
