# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Help documentation for Service Fabric compose commands."""

from knack.help_files import helps

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
    short-summary: Copy a Service Fabric application package to the image 
                   store.
    long-summary: Optionally display upload progress for each file in the
                  package. Upload progress is sent to `stderr`.
    parameters:
        - name: --path
          type: string
          short-summary: Path to local application package
        - name: --show-progress
          type: bool
          short-summary: Show file upload progress for large packages
"""
