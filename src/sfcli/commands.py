"""Command and help loader for the Service Fabric CLI.

Commands are stored as one to one mappings between command line syntax and
python function.
"""

import os

from knack.commands import CLICommandsLoader, CommandSuperGroup
from knack.help import CLIHelp
from sfcli.apiclient import SFApiClient

# Default names
SF_CLI_NAME = 'Azure Service Fabric CLI'
SF_CLI_SHORT_NAME = 'sfcli'
SF_CLI_CONFIG_DIR = os.path.join('~', '.{}'.format(SF_CLI_SHORT_NAME))
SF_CLI_ENV_VAR_PREFIX = SF_CLI_SHORT_NAME

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

        # Generate client
        sf_c = SFApiClient(SF_CLI_CONFIG_DIR, SF_CLI_ENV_VAR_PREFIX)

        with CommandSuperGroup(__name__, self, client_func_path,
                               client_factory=sf_c.client) as super_group:
            with super_group.group('cluster') as group:
                group.command('health', 'get_cluster_health')

    def load_arguments(self, command):
        """Load global arguments for commands"""
