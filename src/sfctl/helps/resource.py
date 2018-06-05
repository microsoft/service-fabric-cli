# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Help documentation for managing Service Fabric Mesh Resources."""

from knack.help_files import helps

helps['resources deployment init'] = """
  type: command
  short-summary: Initialize current context with a YAML file for deployment  
  long-summary: To be filled long summary
"""

helps['resources deployment create'] = """
  type: command
  short-summary: Create a deployment of services  
  long-summary: To be filled long summary
"""

helps['resources deployment delete'] = """
  type: command
  short-summary: Delete multiple services at the same time  
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

helps['resources volumes init'] = """
  type: command
  short-summary: Initialize current context with volumes.yaml
  long-summary: To be filled long summary
"""

helps['resources volumes get'] = """
  type: command
  short-summary: Get information about volume resource from the environment
  long-summary: To be filled long summary
  parameters:
    - name: --volume-resource-name
      type: string
      short-summary: Name of the Volume Resource
"""

helps['resources volumes delete'] = """
  type: command
  short-summary: Delete an volume resources from the environment
  long-summary: To be filled long summary
  parameters:
    - name: --volume-resource-name
      type: string
      short-summary: Name of the Volume Resource
"""

helps['resources network init'] = """
  type: command
  short-summary: Initialize current context with networks.yaml 
  long-summary: To be filled long summary
"""

helps['resources network get'] = """
  type: command
  short-summary: Get information about network resources from the environment
  long-summary: To be filled long summary
"""

helps['resources network delete'] = """
  type: command
  short-summary: Delete an network resources from the environment 
  long-summary: To be filled long summary
"""

helps['resources secrets init'] = """
  type: command
  short-summary: Initialize current context with secrets.yaml  
  long-summary: To be filled long summary
"""

helps['resources secrets get'] = """
  type: command
  short-summary: Get information about secret resources from the environment  
  long-summary: To be filled long summary
"""

helps['resources secrets delete'] = """
  type: command
  short-summary: Delete an secret resources from the environment
  long-summary: To be filled long summary
"""