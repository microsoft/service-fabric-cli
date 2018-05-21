# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Tests to ensure that commands are processed correctly"""

from os import path
import unittest
from contextlib2 import redirect_stdout
from sfctl.params import json_encoded

try:
    # Python 2
    from cStringIO import StringIO
except ImportError:
    # Python 3
    from io import StringIO


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

        # Test .txt files containing json live in the same folder as this file.
        # Get their full paths.
        file_path_correct_json = \
            '@' + path.join(path.dirname(__file__), 'sample_json', 'correct_json.txt')
        file_path_incorrect_json =\
            '@' + path.join(path.dirname(__file__), 'sample_json', 'incorrect_json.txt')
        file_path_empty_file = \
            '@' + path.join(path.dirname(__file__), 'sample_json', 'empty_file.txt')
        file_path_nonexistent = \
            '@' + path.join(path.dirname(__file__), 'sample_json', 'non_existent.txt')

        # Use str_io capture here to avoid the printed clutter when running the tests.
        # Using ValueError instead of json.decoder.JSONDecodeError because that is not
        # supported in python 2.7.
        # Test that incorrect or empty file paths return error.
        str_io = StringIO()
        with redirect_stdout(str_io):
            with self.assertRaises(ValueError):
                json_encoded(file_path_empty_file)
            with self.assertRaises(ValueError):
                json_encoded(file_path_incorrect_json)

        # Test that correct file path returns correct serialized object
        self.assertEqual(dictionary, json_encoded(file_path_correct_json))

        # Test that appropriate error messages are printed out on error

        str_io = StringIO()
        with redirect_stdout(str_io):
            try:
                json_encoded(file_path_empty_file)
            except Exception:  # pylint: disable=broad-except
                pass

        printed_output = str_io.getvalue()

        self.assertIn(
            'Decoding JSON value from file {0} failed'.format(file_path_empty_file.lstrip('@')),
            printed_output)
        self.assertTrue('Expecting value: line 1 column 1 (char 0)' in printed_output
                        or
                        'No JSON object could be decoded' in printed_output)
        self.assertNotIn('You can also pass the json argument in a .txt file', printed_output)

        str_io = StringIO()
        with redirect_stdout(str_io):
            try:
                json_encoded(file_path_incorrect_json)
            except Exception:  # pylint: disable=broad-except
                pass

        printed_output = str_io.getvalue()
        self.assertIn(
            'Decoding JSON value from file {0} failed'.format(file_path_incorrect_json.lstrip('@')),
            printed_output)
        self.assertTrue('Expecting property name enclosed in double quotes: line 1 column 2 (char 1)' in printed_output  # pylint: disable=line-too-long
                        or
                        'Expecting property name: line 1 column 2 (char 1)' in printed_output)
        self.assertNotIn('You can also pass the json argument in a .txt file', printed_output)

        str_io = StringIO()
        with redirect_stdout(str_io):
            try:
                json_encoded(file_path_nonexistent)
            except Exception:  # pylint: disable=broad-except
                pass

        printed_output = str_io.getvalue()
        self.assertIn(
            'File not found at {0}'.format(file_path_nonexistent.lstrip('@')),
            printed_output)

    def test_json_encoded_argument_processing_string_input(self):  # pylint: disable=invalid-name
        """Make sure that method json_encoded in src/params.py correctly:
            - Reads the .txt files
            - If input is not a file, reads and serializes the input as json
            - Returns correct error messages
        """

        # --------------------------------------
        # Pass in json as a string
        # --------------------------------------

        str_io = StringIO()

        # str_io captures the output of a wrongly formatted json
        with redirect_stdout(str_io):
            try:
                json_encoded('')
            except Exception:  # pylint: disable=broad-except
                pass

        printed_output = str_io.getvalue()

        self.assertIn('You can also pass the json argument in a .txt file', printed_output)
        self.assertIn('To do so, set argument value to the '
                      'absolute path of the text file prefixed by "@".', printed_output)

        # str_io captures the output of a wrongly formatted json
        str_io = StringIO()
        with redirect_stdout(str_io):
            try:
                json_encoded('{3.14 : "pie"}')
            except Exception:  # pylint: disable=broad-except
                pass

        printed_output = str_io.getvalue()
        self.assertIn('You can also pass the json argument in a .txt file', printed_output)
        self.assertIn('To do so, set argument value to the '
                      'absolute path of the text file prefixed by "@".', printed_output)

        # Capture output with str_io even though it's not used in order to prevent test to writing
        # to output, in order to keep tests looking clean.
        # These tests ensure that incorrectly formatted json throws error.
        str_io = StringIO()
        with redirect_stdout(str_io):
            with self.assertRaises(ValueError):
                json_encoded('')
            with self.assertRaises(ValueError):
                json_encoded('{3.14 : "pie"}')

        # Test to ensure that correct json is serialized correctly.
        simple_dictionary = {'k': 23}
        self.assertEqual(simple_dictionary, json_encoded('{"k": 23}'))
