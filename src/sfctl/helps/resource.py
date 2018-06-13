# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Help documentation for managing Service Fabric Mesh Resources."""

from knack.help_files import helps

helps['resources deployment create'] = """
  type: command
  short-summary: Create a deployment of services  
  long-summary: To be filled long summary
"""

helps['resources applications init'] = """
  type: command
  short-summary: Initialize current context with applications.yaml
  long-summary: To be filled long summary
  parameters:
    - name: --file-path
      type: string
      short-summary: File path of the yaml file
"""

helps['resources applications get'] = """
  type: command
  short-summary: Get information about application resources from the environment
  long-summary: To be filled long summary
  parameters:
    - name: --application-resource-name
      type: string
      short-summary: Name of the Application Resource
"""

helps['resources applications delete'] = """
  type: command
  short-summary: Delete an application resource from the environment 
  long-summary: To be filled long summary
  parameters:
    - name: --application-resource-name
      type: string
      short-summary: Name of the Application Resource
"""

helps['resources volume init'] = """
  type: command
  short-summary: Initialize current context with volumes.yaml
  long-summary: To be filled long summary
"""

helps['resources volume get'] = """
  type: command
  short-summary: Get information about volume resource from the environment
  long-summary: To be filled long summary
  parameters:
    - name: --volume-resource-name
      type: string
      short-summary: Name of the Volume Resource
"""

helps['resources volume delete'] = """
  type: command
  short-summary: Delete an volume resources from the environment
  long-summary: To be filled long summary
  parameters:
    - name: --volume-resource-name
      type: string
      short-summary: Name of the Volume Resource
"""
