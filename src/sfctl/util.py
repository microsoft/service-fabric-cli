# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Some misc util methods related to the CLI"""

def is_help_command(command):
    """
    Checks that the user inputted command is a help command, which will not go over the wire.
    This is a command with -h or --help.

    The help functionality is triggered no matter where the -h appears in the command (arg ordering)

    :param command: a list of strings representing the command, for example, ['node', 'list', '-h']
    :return: True if it is a help command. False otherwise.
    """

    for segment in command:
        if segment in ('-h', '--help'):
            return True

    return False
