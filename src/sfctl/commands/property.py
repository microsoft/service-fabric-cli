# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------
"""Property related commands"""

from knack import CommandSuperGroup
from sfctl.apiclient import create as create_client

def define_commands(loader):
    """Load property related commands"""
    sdk_func_path = 'azure.servicefabric#ServiceFabricClientAPIs.{}'
    with CommandSuperGroup(__name__, loader, sdk_func_path,
                           client_factory=create_client) as super_group:
        with super_group.group('property') as group:
            group.command('put', 'put_property')
            group.command('list', 'get_property_info_list')
            group.command('get', 'get_property_info')
            group.command('delete', 'delete_property')
