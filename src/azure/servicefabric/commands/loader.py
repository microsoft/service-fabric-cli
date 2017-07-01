"""Command groups for the Service Fabric CLI.

Contains the definitions for all of the commands currently available when using
the command line.

The actual implementation of commands is kept seperate. This module is only
responsible for dispatching the correct functions for each command
"""

import os
import sys
from collections import OrderedDict

from knack.commands import CLICommandsLoader, CommandSuperGroup
from knack.arguments import ArgumentsContext
from knack.help import CLIHelp

from knack.help_files import helps

helps['abc'] = """
    type: group
    short-summary: Manage the alphabet of words.
"""

helps['abc list'] = """
    type: command
    short-summary: List the alphabet.
    examples:
        - name: It's pretty straightforward.
          text: exapp4 abc list
"""

def a_test_command_handler():
    return [{'a': 1, 'b': 1234}, {'a': 3, 'b': 4}]


def abc_list_command_handler():
    import string
    return list(string.ascii_lowercase)

def hello_command_handler(myarg=None, abc=None):
    return ['hello', 'world', myarg, abc]


class SFCommandHelp(CLIHelp):

    def __init__(self, ctx=None):
        super(SFCommandHelp, self).__init__(ctx=ctx)

class SFCommandLoader(CLICommandsLoader):

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
