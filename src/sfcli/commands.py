"""Command and help loader for the Service Fabric CLI.

Commands are stored as one to one mappings between command line syntax and
python function.
"""

from collections import OrderedDict
from knack.commands import CLICommandsLoader, CommandSuperGroup
from knack.help import CLIHelp
from knack.arguments import ArgumentsContext
from sfcli.apiclient import create as client_create
# Need to import so global help dict gets updated
import sfcli.helps.app # pylint: disable=unused-import

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

        with CommandSuperGroup(__name__, self, 'sfcli.custom_app#{}',
                               client_factory=client_create) as super_group:
            with super_group.group('compose') as group:
                group.command('create', 'create_compose_application')
            with super_group.group('application') as group:
                group.command('upload', 'upload')
                group.command('create', 'create')
                group.command('upgrade', 'upgrade')

        with CommandSuperGroup(__name__, self, 'sfcli.custom_cluster#{}',
                               client_factory=client_create) as super_group:
            with super_group.group('cluster') as group:
                group.command('select', 'select')

        with CommandSuperGroup(__name__, self, 'sfcli.custom_chaos#{}',
                               client_factory=client_create) as super_group:
            with super_group.group('chaos') as group:
                group.command('start', 'start')

        with CommandSuperGroup(__name__, self, 'sfcli.custom_health#{}',
                               client_factory=client_create) as super_group:
            with super_group.group('application') as group:
                group.command('report-health', 'report_app_health')
            with super_group.group('service') as group:
                group.command('report-health', 'report_svc_health')
            with super_group.group('partition') as group:
                group.command('report-health', 'report_partition_health')
            with super_group.group('replica') as group:
                group.command('report-health', 'report_replica_health')
            with super_group.group('node') as group:
                group.command('report-health', 'report_node_health')

        with CommandSuperGroup(__name__, self, 'sfcli.custom_service#{}',
                               client_factory=client_create) as super_group:
            with super_group.group('service') as group:
                group.command('create', 'create')
                group.command('update', 'update')
                group.command('package-upload', 'package_upload')

        return OrderedDict(self.command_table)

    def load_arguments(self, command):
        """Load specialized arguments for commands"""

        with ArgumentsContext(self, '') as arg_context:
            arg_context.argument('timeout', type=int, default=60,
                                 options_list=('-t', '--timeout'),
                                 help='Server timeout in seconds')
        super(SFCommandLoader, self).load_arguments(command)
