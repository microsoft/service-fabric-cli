"""Command and help loader for the Service Fabric CLI.

Commands are stored as one to one mappings between command line syntax and
python function.
"""

from collections import OrderedDict
from knack.commands import CLICommandsLoader, CommandSuperGroup
from knack.help import CLIHelp
from sfcli.apiclient import create as client_create
# Need to import so global help dict gets updated
import sfcli.helps.compose

class SFCommandHelp(CLIHelp):
    """Service Fabric CLI help loader"""

    def __init__(self, ctx=None):
        header_msg = 'Service Fabric Command Line'

        super(SFCommandHelp, self).__init__(ctx=ctx,
                                            welcome_message=header_msg)

class SFCommandLoader(CLICommandsLoader):
    """Service Fabric CLI command loader, containing command mappings"""

    def load_command_table(self, args):
        """Load all Service Fabric commands"""

        client_func_path = 'azure.servicefabric#ServiceFabricClientAPIs.{}'
        with CommandSuperGroup(__name__, self, client_func_path,
                               client_factory=client_create) as super_group:
            with super_group.group('cluster') as group:
                group.command('health', 'get_cluster_health')
        

        # Custom commands

        custom_app_path = 'sfcli.custom_app#{}'
        with CommandSuperGroup(__name__, self, custom_app_path,
                               client_factory=client_create) as super_group:
            with super_group.group('compose') as group:
                group.command('create', 'create_compose_application')

        return OrderedDict(self.command_table)

    def load_arguments(self, command):
        """Load global arguments for commands"""
