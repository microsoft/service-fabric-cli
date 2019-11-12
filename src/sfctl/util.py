# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Some misc util methods related to the CLI"""

from six.moves import input as compat_input

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

def get_user_confirmation(prompt):
    """
    Prompt user for confirmation. Return True if user confirms. False otherwise.
    Keep prompting until user gives either yes or no

    :param prompt: (str) The prompt for users. For example: about to delete, confirm?

    :return: bool. True is user confirms, False otherwise
    """

    confirmed = compat_input(prompt)

    while confirmed.lower() not in ['y', 'yes', 'n', 'no']:
        confirmed = compat_input(prompt)

    return confirmed.lower() in ['y', 'yes']
