# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Custom commands for the Service Fabric infrastructure service support"""

def is_command(client, command_input, service_id=None, timeout=60):
    """Invokes an administrative command on the given Infrastructure Service
    instance.
    """
    client.invoke_infrastructure_command(command_input, service_id, timeout)

def is_query(client, command_input, service_id=None, timeout=60):
    """Invokes a read-only query on the given infrastructure service instance.
    """
    client.invoke_infrastructure_query(command_input, service_id, timeout)
