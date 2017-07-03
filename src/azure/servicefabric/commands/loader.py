"""Command and help loader for the Service Fabric CLI.

Commands are stored as one to one mappings between command line syntax and
python function.
"""

from collections import OrderedDict

from knack.commands import CLICommandsLoader, CommandSuperGroup
from knack.arguments import ArgumentsContext
from knack.help import CLIHelp

# Need to import so global help dict gets updated
import azure.servicefabric.commands.helps  # pylint: disable=unused-import


class SFCommandHelp(CLIHelp):
    """Service Fabric CLI help loader"""

    def __init__(self, ctx=None):
        header_msg = 'Service Fabric Command Line'

        super(SFCommandHelp, self).__init__(ctx=ctx,
                                            welcome_message=header_msg)

class SFCommandLoader(CLICommandsLoader):
    """Service Fabric CLI command loader, containing command mappings"""

    def load_command_table(self, args):


        with CommandSuperGroup(__name__, self, '__main__#{}') as sg:
            with sg.group('hello') as g:
                g.command('world', 'hello_command_handler', confirmation=True)
            with sg.group('abc') as g:
                g.command('list', 'abc_list_command_handler')
                g.command('show', 'a_test_command_handler')
        return OrderedDict(self.command_table)

    def load_arguments(self, command):
        with ArgumentsContext(self, 'hello world') as ac:
            ac.argument('myarg', type=int, default=100)
        super(SFCommandLoader, self).load_arguments(command)
