# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Tests to ensure that commands are processed correctly"""

from os import path
from contextlib2 import redirect_stdout
from io import StringIO
import unittest
from sfctl.params import json_encoded


class CommandsProcessTests(unittest.TestCase):
    """Processing commands tests"""

    def test_json_encoded_argument_processing_file_input(self):  # pylint: disable=invalid-name
        """Make sure that method json_encoded in src/params.py correctly:
            - Reads the .txt files
            - If input is not a file, reads and serializes the input as json
            - Returns correct error messages
        """

        # --------------------------------------
        # Pass in json as a file
        # --------------------------------------

        # Create object that contains the correct object that should be loaded from reading the file
        pets_dictionary = dict()
        pets_dictionary['Coco'] = 'Golden Retriever'
        pets_dictionary['Lily'] = 'Ragdoll Cat'
        pets_dictionary['Poofy'] = 'Golden Doodle'

        dictionary = dict()
        dictionary['name'] = 'John'
        dictionary['last_name'] = 'Smith'
        dictionary['pets'] = pets_dictionary

        file_path_correct_json = path.join(path.dirname(__file__), 'correct_json.txt')
        file_path_incorrect_json = path.join(path.dirname(__file__), 'incorrect_json.txt')
        file_path_empty_file = path.join(path.dirname(__file__), 'empty_file.txt')

        # Use this here to avoid the printed clutter when running the tests.
        # Using ValueError instead of json.decoder.JSONDecodeError because that is not
        # supported in python 2.7
        str_io = StringIO()
        with redirect_stdout(str_io):
            with self.assertRaises(ValueError):
                json_encoded(file_path_empty_file)
            with self.assertRaises(ValueError):
                json_encoded(file_path_incorrect_json)

        self.assertEqual(dictionary, json_encoded(file_path_correct_json))

        # Test that appropriate error messages are printed out on error

        str_io = StringIO()
        with redirect_stdout(str_io):
            try:
                json_encoded(file_path_empty_file)
            except Exception:  # pylint: disable=broad-except
                pass

        printed_output = str_io.getvalue()
        self.assertIn('Decoding JSON value from file {0} failed'.format(file_path_empty_file),
                      printed_output)
        self.assertIn('Expecting value: line 1 column 1 (char 0)', printed_output)
        self.assertNotIn('Hint: You can also pass the json argument in a .txt file', printed_output)

        str_io = StringIO()
        with redirect_stdout(str_io):
            try:
                json_encoded(file_path_incorrect_json)
            except Exception:  # pylint: disable=broad-except
                pass

        printed_output = str_io.getvalue()
        self.assertIn('Decoding JSON value from file {0} failed'.format(file_path_incorrect_json),
                      printed_output)
        self.assertIn('Expecting property name enclosed in double quotes: line 1 column 2 (char 1)',
                      printed_output)
        self.assertNotIn('Hint: You can also pass the json argument in a .txt file', printed_output)

    def test_json_encoded_argument_processing_string_input(self):  # pylint: disable=invalid-name
        """Make sure that method json_encoded in src/params.py correctly:
            - Reads the .txt files
            - If input is not a file, reads and serializes the input as json
            - Returns correct error messages
        """

        # --------------------------------------
        # Pass in json as a string
        # --------------------------------------

        simple_dictionary = {'k': 23}

        str_io = StringIO()

        with redirect_stdout(str_io):
            try:
                json_encoded('')
            except Exception:  # pylint: disable=broad-except
                pass

        printed_output = str_io.getvalue()
        self.assertIn('Hint: You can also pass the json argument in a .txt file', printed_output)
        self.assertIn('To do so, set argument value to the relative or '
                      'absolute path of the text file', printed_output)

        str_io = StringIO()
        with redirect_stdout(str_io):
            try:
                json_encoded('{3.14 : "pie"}')
            except Exception:  # pylint: disable=broad-except
                pass

        printed_output = str_io.getvalue()
        self.assertIn('Hint: You can also pass the json argument in a .txt file', printed_output)
        self.assertIn('To do so, set argument value to the relative or '
                      'absolute path of the text file', printed_output)

        # Use this here to avoid the printed clutter when running the tests.
        str_io = StringIO()
        with redirect_stdout(str_io):
            with self.assertRaises(ValueError):
                json_encoded('')
            with self.assertRaises(ValueError):
                json_encoded('{3.14 : "pie"}')

        self.assertEqual(simple_dictionary, json_encoded('{"k": 23}'))
