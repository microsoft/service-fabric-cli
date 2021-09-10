# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Tests that the text provided as custom help text is always up tp date.
Check the help text defined in the helps section appear in the service fabric Python SDK.
This will check that custom help text is always up to date with those defined in
Service Fabric Swagger specifications.

This does not test for missing information. In the future, consider requiring long summaries
for all descriptions."""

from __future__ import print_function
import unittest
from os import listdir
from os.path import dirname, join, abspath, pardir
from imp import load_source

CURRENT_DIR = dirname(abspath(__file__))  # This should be <location>/src/sfctl/tests
SRC_PARENT_DIR = dirname(dirname(dirname(CURRENT_DIR)))
CUSTOM_SDK_HELPER_FILE = join(SRC_PARENT_DIR, 'scripts', 'check_and_use_custom_sdk.py')

load_source('custom_sdk_helper', CUSTOM_SDK_HELPER_FILE)

import custom_sdk_helper  # pylint: disable=wrong-import-position,import-error


class CustomHelpTextCorrectnessTests(unittest.TestCase):
    """Tests that the text provided as custom help text is always up to date."""

    # If a line from a customs helps file starts with the following, do not validate.
    # This list should eventually become empty since we want to validate all help
    # text. These are lines which we know will fail validation, but through various
    # fixes in the future, should pass.
    exclusion_list = [
        '"possible values include',
        'possible values include',
        'Path to the target Docker Compose file',  # This and following is custom - not in swagger
        'can be retrieved by \'service code-package-list\''
    ]

    @staticmethod
    def _get_path_SDK_files():  # pylint: disable=invalid-name
        """
        Find the location of the python SDK folder which will be used for testing
        :return: string representing the absolute path
        """

        # path_to_root is the abs path to the folder which contains the 'src' folder.
        path_to_root = dirname(dirname(dirname(__file__)))

        custom_sdk_path = custom_sdk_helper.get_custom_sdk_path(path_to_root)  # Full path
        should_use_custom_sdk = custom_sdk_helper.check_if_should_use_custom_sdk(custom_sdk_path)

        if should_use_custom_sdk:
            return custom_sdk_path

        site_packages = custom_sdk_helper.get_path_public_sdk()  # full path to site packages
        return join(site_packages, 'azure', 'servicefabric')

    @staticmethod
    def _read_python_sdk():
        """
        Find the location of the python SDK's apis (find file service_fabric_client_ap_is.py)
        Find the location of the python SDK's models (in same parent folder of the file above)

        Return a list of strings, which represent all the comments in the found
        python files as strings.

        For each python file found, read the entire file, and return all text which appears
        as text in the python file as one joined line.

        In the future, for optimization, this should return only docstring text, rather than
        all text in the given python file.

        Each text line is stripped and joined with one white space in the middle.

        :return: List[string] with each string representing the text found in each
        python file in the python SDK. One string per file.
        """

        doc_strings = []  # The return value

        sdk_path = CustomHelpTextCorrectnessTests._get_path_SDK_files()

        # A list of strings containing abs paths to the SDK api file and model files
        # start off containing the SDK API file
        # List of strings
        # Only one service_fabric_client_ap_is.py should exist but can appear differently depending on if its custom sdk
        # or if its the official release.
        sdk_files_path = [join(sdk_path, '_service_fabric_client_ap_is.py'),
                          join(sdk_path, 'service_fabric_client_ap_is.py')]

        # Add all the models files
        models_path = join(sdk_path, 'models')
        for file_name in listdir(models_path):
            if file_name.endswith('.py'):
                sdk_files_path.append(join(models_path, file_name))

        for python_file_path in sdk_files_path:
            try:
                lines = [line.strip() for line in open(python_file_path)]
                doc_strings.append(' '.join(lines).lower())
            except: # pylint: disable=bare-except
                print("missing - {0}".format(python_file_path))

        return doc_strings

    @staticmethod
    def _get_helps_folder():
        """Gets the absolute path of the helps folder which contains
        all the custom help text files.
        :return: string"""

        current_dir = dirname(__file__)
        return abspath(join(current_dir, pardir, 'helps'))

    @staticmethod
    def _read_custom_help_lines():
        """
        Read the custom help files. Parse each file for the following:

            Read in:
                short-summary:
                long-summary:


            Ignore:
                type:
                - name:
                parameters:
                examples:

        Here, parse means that if you see a line starting with one of the starters listed above,
        read in all the text after it until you hit another starter text.

        Lowercase all lines.

        :return: List[string] with each string representing one item from short-summary or
        long-summary
        """

        # The returned list
        help_text_lines = []

        # The line prefixes
        read_value = ['short-summary:', 'long-summary:']
        ignore = ['type:', '- name:', 'parameters:', 'examples:', '"""']

        # Get a list of all the relevant files in the helps folder
        helps_folder = CustomHelpTextCorrectnessTests._get_helps_folder()
        help_files_path = []
        for file_name in listdir(helps_folder):
            # Ignore the init file and the main file
            if file_name.endswith('.py') and not file_name.startswith(('__init__', 'main')):
                help_files_path.append(join(helps_folder, file_name))

        # Read each file
        for python_file_path in help_files_path:
            with open(python_file_path) as python_file:

                lines = python_file.readlines()
                current_string = ''
                ignoring = True  # Start with true because there is code in the file first

                for line in lines:
                    line = line.strip()

                    if line.startswith(tuple(ignore)):

                        if current_string.strip() != '':
                            cleaned_up_current_string = current_string.strip().lower()
                            if not cleaned_up_current_string.startswith(
                                    tuple(CustomHelpTextCorrectnessTests.exclusion_list)):
                                help_text_lines.append(cleaned_up_current_string)

                        current_string = ''
                        ignoring = True

                    elif line.startswith(tuple(read_value)):

                        if current_string.strip() != '':
                            cleaned_up_current_string = current_string.strip().lower()
                            if not cleaned_up_current_string.startswith(
                                    tuple(CustomHelpTextCorrectnessTests.exclusion_list)):
                                help_text_lines.append(cleaned_up_current_string)

                        current_string = line.lstrip('short-summary:')
                        current_string = current_string.lstrip('long-summary:').strip()
                        ignoring = False

                    else:
                        if ignoring:
                            continue
                        current_string += ' ' + line

        return help_text_lines

    def test_custom_help_text(self):
        """
        This actually runs the test to make sure that help text is up to date with swagger.

        In the assert line, we allow a certain number of mismatched lines. This is because
        in some instances, swagger text is not appropriate for sfctl.
        :return:
        """

        custom_help_lines = CustomHelpTextCorrectnessTests._read_custom_help_lines()
        python_sdk_lines = CustomHelpTextCorrectnessTests._read_python_sdk()

        lines_not_found = []

        for custom_help_line in custom_help_lines:
            line_found = False
            for sdk_line in python_sdk_lines:
                if custom_help_line in sdk_line:
                    line_found = True
                    break

            if not line_found:
                lines_not_found.append(custom_help_line)

        print('The following lines from custom help files do not have a corresponding '
              'Swagger definition. This probably means that it is outdated. Please update and '
              're-run the test. If the help text should be custom, update the allowances in '
              'this test.')
        for line in lines_not_found:
            print()
            print(line)

        allowable_lines_not_found = [148, 89]

        print()
        print('The total number of lines compared is ' + str(len(custom_help_lines)))
        print('The total number of lines not found is ' + str(len(lines_not_found)))
        print('The total number of allowable lines not found is ' + str(allowable_lines_not_found))
        print('The total number of excluded lines is ' +
              str(len(CustomHelpTextCorrectnessTests.exclusion_list)))

        # Assert if there are any lines which do not match.
        self.assertTrue(len(lines_not_found) in allowable_lines_not_found,
                        msg='The allowable mismatched documentation lines does not match the actual number.')
