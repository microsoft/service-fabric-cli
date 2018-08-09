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
  parameters:
    - name: --file-path
      type: string
      short-summary: Comma seperated file paths of all the yaml files
"""

helps['resources deployment validate'] = """
  type: command
  short-summary: Validates the deployment of services
  long-summary: To be filled long summary
  parameters:
    - name: --file-path
      type: string
      short-summary: Comma seperated file paths of all the yaml files
"""

helps['resources application get'] = """
  type: command
  short-summary: Get information about application resources from the environment
  long-summary: To be filled long summary
  parameters:
    - name: --application-resource-name
      type: string
      short-summary: Name of the Application Resource
"""

helps['resources application delete'] = """
  type: command
  short-summary: Delete an application resource from the environment 
  long-summary: To be filled long summary
  parameters:
    - name: --application-resource-name
      type: string
      short-summary: Name of the Application Resource
"""

helps['resources service list'] = """
  type: command
  short-summary: List all services of an application resource
  long-summary: To be filled long summary
  parameters:
    - name: --application-resource-name
      type: string
      short-summary: Name of the Application Resource
"""

helps['resources service get'] = """
  type: command
  short-summary: Get information about a service of an application resource
  long-summary: To be filled long summary
  parameters:
    - name: --application-resource-name
      type: string
      short-summary: Name of the Application Resource
    - name: --service-resource-name
      type: string
      short-summary: Name of the Service Resource
"""

helps['resources service-replica list'] = """
  type: command
  short-summary: List all replicas of a service in an application resource
  long-summary: To be filled long summary
  parameters:
    - name: --application-resource-name
      type: string
      short-summary: Name of the Application Resource
    - name: --service-resource-name
      type: string
      short-summary: Name of the Service Resource
"""

helps['resources service-replica get'] = """
  type: command
  short-summary: Get the information of a replica of a service in an application resource
  long-summary: To be filled long summary
  parameters:
    - name: --application-resource-name
      type: string
      short-summary: Name of the Application Resource
    - name: --service-resource-name
      type: string
      short-summary: Name of the Service Resource
    - name: --replica-name
      type: string
      short-summary: Name of the replica
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
