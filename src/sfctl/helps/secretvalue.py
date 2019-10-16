# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Help documentation for Service Fabric mesh secretvalue commands."""

from knack.help_files import helps

# If the parameter name doesn't match the actual parameter name,
# no information will be provided in the help page

# To keep newlines in the help documentation, follow this format:
# long-summary: |
#    Following are the ...
#    1. text
#    2. text

helps['mesh secretvalue show'] = """
    type: command
    short-summary: Lists the specified value of the secret resource.
    parameters:
        - name: --secret-resource-name
          type: string
          short-summary: The name of the secret resource.
        - name: --secret-value-resource-name
          type: string
          short-summary: Version identifier of the secret value
        - name: --show-value
          type: bool
          short-summary: Show the actual value of the secret version
"""
