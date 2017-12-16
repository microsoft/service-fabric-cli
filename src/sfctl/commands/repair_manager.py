# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------
"""Repair manager related commands"""

from knack import CommandSuperGroup
from sfctl.apiclient import create as create_client

def define_commands(loader):
    """Load repair manager related commands"""
    sdk_func_path = 'azure.servicefabric#ServiceFabricClientAPIs.{}'
    with CommandSuperGroup(__name__, loader, sdk_func_path,
                           client_factory=create_client) as super_group:
        with super_group.group('rpm') as group:
            group.command('delete', 'delete_repair_task')
            group.command('list', 'get_repair_task_list')
            group.command('approve-force', 'force_approve_repair_task')
