# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Tests that -h does not return error and has all required text.
This only tests for commands/subgroups which are specified in this file."""

from __future__ import print_function
import unittest
from subprocess import Popen, PIPE


class HelpTextTests(unittest.TestCase):
    """Tests that -h does not return error and includes all help text."""

    def _validate_output_read_line(self,  # pylint: disable=too-many-arguments
                                   command_input, line,
                                   section, subgroups, commands,
                                   subgroups_index, commands_index):
        """ Read a line of text and validates it for correctness.
        Parameter line (string) should be unprocessed. For example, the line should not be
        stripped of starting or trailing white spaces.

        This method returns the updated values of subgroups_index and commands_index as a tuple.
        Tuple has ordering (subgroups_index, commands_index).
        If an error occurs during validation, an assert is called. """

        line = line.strip()

        if (section == 'Command') or (section == 'Group'):
            # if the line starts with the inputted command, then it describes the command.
            # make sure the line has text after it
            if line.startswith(command_input):
                self.assertGreater(
                    len(line),
                    len(command_input),
                    msg='Validating help output failed on line: ' + line)

            return subgroups_index, commands_index

        elif section == 'Arguments':
            # For lines that start with '--' (for argument descriptions), make sure that
            # there is something after the argument declaration
            if line.startswith('--'):
                self.assertIn(': ', line,
                              msg='Validating help output failed on line: ' + line)

                # Find the first ':' character and check that there are characters following it
                first_index = line.find(': ')
                self.assertGreater(
                    len(line),
                    first_index + 1,
                    msg='Validating help output failed on line: ' + line)

            return subgroups_index, commands_index

        elif (section == 'Commands') or (section == 'Subgroups'):
            # Make sure that if the line starts with the command/group in
            # the expected tuple, that a description follows it.
            # The line will either start with the name provided in the expected tuple,
            # or it will be a continuation line. Ignore continuation lines.
            first_word_of_line = line.split()[0].rstrip(':')

            if section == 'Commands':

                # If we've reached the end of the commands tuple, then skip, since everything
                # after this is a continuation line.
                if len(commands) == commands_index:
                    return subgroups_index, commands_index

                self.assertGreater(len(commands), commands_index,
                                   msg='None or missing expected commands provided in test for ' + command_input)  # pylint: disable=line-too-long
                if first_word_of_line == commands[commands_index]:
                    # make sure there is descriptive text in this line by checking
                    # that the line is longer than just the command.
                    self.assertGreater(
                        len(line),
                        len(first_word_of_line),
                        msg='Validating help text failed in "Commands" on line: ' + line)

                    commands_index += 1

            elif section == 'Subgroups':

                # If we've reached the end of the commands tuple, then skip
                if len(subgroups) == subgroups_index:
                    return subgroups_index, commands_index

                self.assertGreater(len(subgroups), subgroups_index,
                                   msg='None or missing expected subgroups provided in test for ' + command_input)  # pylint: disable=line-too-long
                if first_word_of_line == subgroups[subgroups_index]:
                    # make sure there is descriptive text in this line
                    self.assertGreater(
                        len(line),
                        len(first_word_of_line),
                        msg='Validating help text failed in "Subgroups" on line: ' + line)

                    subgroups_index += 1

            return subgroups_index, commands_index

        else:
            self.fail('Section name {0} is not supported'.format(section))
            # The following line will be reached. It is added so pylint does not complain
            # about inconsistent-return-statements.
            return subgroups_index, commands_index

    @classmethod
    def _validate_output_read_section_name(cls, line):
        """ Read a given line and validate it for correctness based on the given section.
        Parameter line (string) should be unprocessed. For example, the line should not be
        stripped of starting or trailing white spaces.

        Returns the section name if the given line designates the beginning of a new section.
        Returns None if the line does not. """

        if line.strip() and not line[0].isspace():
            # Use these lines to set the 'section' variable and move on to the next line
            line = line.strip().rstrip(':')
            if line == 'Commands':
                return 'Commands'
            elif (line == 'Arguments') or (line == 'Global Arguments'):
                return 'Arguments'
            elif line == 'Group':
                return 'Group'
            elif line == 'Subgroups':
                return 'Subgroups'
            elif line == 'Command':
                return 'Command'
        return None

    def validate_output(self, command_input, subgroups=(), commands=()):  # pylint: disable=too-many-locals
        """
        This function verifies that the returned help text is correct, and that no exceptions
        are thrown during invocation. If commands are provided, this function will call itself
        recursively to verify the correctness of the commands. It verifies correctness by:

        - All listed subgroups and commands appear in alphabetical order. We do not check for the
            existence of extra subgroups and commands.
        - If subgroups or commands are not provided, then we expect it not to appear in
            the help text. If it does, there will be an assertion raised in this test.
        - All listed groups/subgroups, commands, and arguments have descriptive text

        Limitations: This test doesn't search for new commands which are added.
                     If a test entry is not added here, then that entry will not be
                     verified.

        command_input (string): This represents the command for which you want to get the help text.
            For example, "sfctl" or "sfctl application" or "sfctl application list".
            Parameter command_input should not include the "-h" to get the help text, as this
            method will take care of that.

        subgroups (tuple of strings): This represents all of the subgroups expected in the
            help text. This tuple must be in alphabetical order.

        commands (tuple of strings): This represents all of the commands expected in the
            help text. This tuple must be in alphabetical order.

        Help text has two formats. One for groups, and one for commands.
        """

        help_command = command_input + ' -h'

        err = None
        returned_string = None

        try:
            # This variable tracks what sections of the help text we are in
            # Possibilities are Group, Subgroups, Commands, Command, Arguments,
            # and Global Arguments.
            # Once we no longer support python 2, change section options of enums
            section = 'Start'

            # A tracker to know how many subgroups or commands have appeared in help text so far
            # We use this to make sure that all expected items are returned
            subgroups_index = 0
            commands_index = 0

            # Call the provided command in command line
            # Do not split the help_command, as that breaks behavior:
            # Linux ignores the splits and takes only the first.
            pipe = Popen(help_command, shell=True, stdout=PIPE, stderr=PIPE)
            # returned_string and err are returned as bytes
            (returned_string, err) = pipe.communicate()

            if err:
                err = err.decode('utf-8')
                self.assertEqual(b'', err, msg='ERROR: in command: ' + help_command)

            if not returned_string:
                self.fail('No help text in command: ' + help_command)

            returned_string = returned_string.decode('utf-8')
            lines = returned_string.splitlines()

            for line in lines:

                if not line.strip():
                    continue

                # Check if we want to mark the start of a new section
                # Check this by seeing if the line is a top level description, ie: 'Commands:'
                # These are characterized by a new line with text starting without white space.
                read_section_output = self._validate_output_read_section_name(line)
                if read_section_output is not None:
                    section = read_section_output

                    # If this line is a section start, no additional processing
                    # is required. Move on to the next line.
                    continue

                # If this line is not a section start, then validate the correctness of the line.
                # This command returns a tuple which includes counters for subgroups and commands
                # which count how many instances of each have been processed.
                updated_indices = self._validate_output_read_line(command_input, line, section,
                                                                  subgroups, commands,
                                                                  subgroups_index,
                                                                  commands_index)
                subgroups_index = updated_indices[0]
                commands_index = updated_indices[1]

            # If section is still 'Start', the something has gone wrong.
            # It means that lines were not processed
            # correctly, since we expect some sections to appear.
            self.assertNotEqual(
                'Start',
                section,
                msg='Command {0}: incomplete help text: {1}'.format(help_command, returned_string))

            # Check that we have traversed completely through both
            # subgroups and commands
            self.assertEqual(len(commands), commands_index,
                             msg=('Not all commands listed in help text for '
                                  + help_command
                                  + '. This may be a problem due incorrect expected ordering.'))
            self.assertEqual(len(subgroups), subgroups_index,
                             msg=('Not all subgroups listed in help text for '
                                  + help_command
                                  + '. This may be a problem due incorrect expected ordering.'))

        except Exception as exception:  # pylint: disable=broad-except
            if not err:
                self.fail(msg='ERROR: Command {0} returned error at execution. Output: {1} Error: {2}'.format(help_command, returned_string, str(exception)))  # pylint: disable=line-too-long
            else:
                self.fail(msg='ERROR: Command {0} returned error at execution. Output: {1} Error: {2}'.format(help_command, returned_string, err))  # pylint: disable=line-too-long

        # Once validation is done for the provided command_input,
        # if there are any commands returned in the help text, validate those commands.
        for command in commands:
            self.validate_output(command_input + ' ' + command)

    def test_help_documentation(self):
        """ Tests all help documentation to ensure that all commands have help text.
        This does not test for typos / correctness in the text itself.
        This test calls validate_output on all commands which sfctl has, without the
        '-h' flag included. The flag will be added by validate_ouput.

        Note: validate_output expects subgroups and commands in order. If out of alphabetical
        order, you will see an error for not all commands/subgroups being listed.

        Note: you do not need to call individual commands. Commands listed in the
        'commands' list will be called and verified automatically. You DO need
        an entry for each subgroup."""

        self.validate_output(
            'sfctl',
            subgroups=('application', 'chaos', 'cluster', 'compose', 'is', 'node',
                       'partition', 'property', 'replica', 'rpm', 'sa-cluster',
                       'service', 'store'))

        self.validate_output(
            'sfctl application',
            commands=('create', 'delete', 'deployed', 'deployed-health', 'deployed-list',
                      'health', 'info', 'list', 'load', 'manifest', 'provision',
                      'report-health', 'type', 'type-list', 'unprovision', 'upgrade',
                      'upgrade-resume', 'upgrade-rollback', 'upgrade-status', 'upload'))

        self.validate_output(
            'sfctl chaos',
            commands=('events', 'get', 'start', 'stop'))

        self.validate_output(
            'sfctl chaos schedule',
            commands=('get', 'set'))

        self.validate_output(
            'sfctl cluster',
            commands=('code-versions', 'config-versions', 'health', 'manifest',
                      'operation-cancel', 'operation-list', 'provision', 'recover-system',
                      'report-health', 'select', 'unprovision', 'upgrade', 'upgrade-resume',
                      'upgrade-rollback', 'upgrade-status', 'upgrade-update'))

        self.validate_output(
            'sfctl container',
            commands=('invoke-api', 'logs'))

        self.validate_output(
            'sfctl compose',
            commands=('create', 'list', 'remove', 'status', 'upgrade', 'upgrade-status'))

        self.validate_output(
            'sfctl is',
            commands=('command', 'query'))

        self.validate_output(
            'sfctl node',
            commands=('disable', 'enable', 'health', 'info', 'list', 'load', 'remove-state',
                      'report-health', 'restart', 'transition', 'transition-status'))

        self.validate_output(
            'sfctl partition',
            commands=('data-loss', 'data-loss-status',
                      'health', 'info', 'list', 'load', 'load-reset', 'quorum-loss',
                      'quorum-loss-status', 'recover', 'recover-all', 'report-health', 'restart',
                      'restart-status', 'svc-name'))

        self.validate_output(
            'sfctl property',
            commands=('delete', 'get', 'list', 'put'))

        self.validate_output(
            'sfctl replica',
            commands=('deployed', 'deployed-list', 'health', 'info', 'list', 'remove',
                      'report-health', 'restart'))

        self.validate_output(
            'sfctl rpm',
            commands=('approve-force', 'delete', 'list'))

        self.validate_output(
            'sfctl sa-cluster',
            commands=('config', 'config-upgrade', 'upgrade-status'))

        self.validate_output(
            'sfctl service',
            commands=('app-name', 'code-package-list', 'create', 'delete', 'deployed-type',
                      'deployed-type-list', 'description', 'get-container-logs',
                      'health', 'info', 'list', 'manifest', 'package-deploy',
                      'package-health', 'package-info', 'package-list', 'recover',
                      'report-health', 'resolve', 'type-list', 'update'))

        self.validate_output(
            'sfctl store',
            commands=('delete', 'root-info', 'stat'))
