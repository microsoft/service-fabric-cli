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
    short-summary: Retrieve the value of a specified version of a secret resource
    long-summary: Retrieve the value of a specified version of a secret resource. 
      Use the --show-value flag to see the actual value
    parameters:
        - name: --secret-resource-name
          type: string
          short-summary: The name of the secret resource.
        - name: --secret-value-resource-name
          type: string
          short-summary: Version identifier of the secret value
            package to
        - name: --show-value
          type: bool
          short-summary: Show file upload progress for large packages
"""