# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Help documentation for sfctl settings commands."""

from knack.help_files import helps

# If the parameter name doesn't match the actual parameter name,
# no information will be provided in the help page

# To keep newlines in the help documentation, follow this format:
# long-summary: |
#    Following are the ...
#    1. text
#    2. text

helps['settings telemetry set-telemetry'] = """
    type: command
    short-summary: Turn on or off telemetry.
    parameters:
        - name: --off
          type: bool
          short-summary: Turn off telemetry. 
        - name: --on
          type: bool
          short-summary: Turn on telemetry.
        

    examples: 
        - name: Turn off telemetry.
          text: sfctl settings telemetry set_telemetry --off
        - name: Turn on telemetry.
          text: sfctl settings telemetry set_telemetry --on
"""
