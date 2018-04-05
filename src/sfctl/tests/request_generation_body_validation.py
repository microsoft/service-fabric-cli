# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Functions to validate that the body of a HTTP request is correct
according to that request's expectations."""

from __future__ import print_function
from sys import stderr


def validate_dictionary_value(command, dict_key, actual_body, expected_body):
    """ Print error message for validation failure and return True
        if validation passed, and False otherwise.
        This function expects that actual_body and expected_body are
        dictionaries. The command parameter is a string that identifies
        which command this is validating. """

    if actual_body[dict_key] != expected_body[dict_key]:
        print(
            'sfctl {0} failed: actual {1}={2}, expected={3}'.format(
                command,
                dict_key,
                actual_body[dict_key],
                expected_body[dict_key]),
            file=stderr)
        return False
    return True


def validate_flat_dictionary(command, actual_body, expected_body):
    """ Validate that two dictionaries, actual_body and expected_body,
        have the same keys and values. Return True if they are the same.
        False otherwise.
        Prints an error message to stderr to show which command and
        which comparison failed."""

    if len(actual_body) != len(expected_body):
        print('Number of items in expected body does not match actual body', file=stderr)
        print('Expected body: {0}'.format(expected_body), file=stderr)
        print('Actual body: {0}'.format(actual_body), file=stderr)
        return False

    for key in expected_body:
        if not validate_dictionary_value(command, key,
                                         actual_body, expected_body):
            return False
    return True
