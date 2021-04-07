# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Functions to validate that the body of a HTTP request is correct
according to that request's expectations."""

from __future__ import print_function
from sys import stderr


def _check_and_print_matching_error(command, dict_key, actual, expected):
    """
    Print error message iff actual != expected.

    :param command: The command
    :param dict_key: The key being matched
    :param actual: Actual value - any type comparable to the expected type
    :param expected: Expected value - any type comparable to the actual type
    :return: Return False if the expected and actual values don't match. True otherwise.
    """
    if actual != expected:
        print(
            'sfctl {0} failed: actual {1}={2}, expected={3}'.format(
                command,
                dict_key,
                actual,
                expected),
            file=stderr)
        return False
    return True


def validate_dictionary_value(command, dict_key, actual_body, expected_body):
    """ Print error message for validation failure and return True
        if validation passed, and False otherwise.
        This function expects that actual_body and expected_body are
        dictionaries. The command parameter is a string that identifies
        which command this is validating. """

    return _check_and_print_matching_error(command, dict_key,
                                           actual_body[dict_key], expected_body[dict_key])

def validate_list_of_objects(command, actual_body, expected_body):
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

    if isinstance(expected_body, list):
        return _check_and_print_matching_error(command, expected_body, expected_body, actual_body)


    for index, _ in enumerate(expected_body):
        actual_body_dictionary = actual_body[index]
        for key in expected_body[index]:
            if not validate_dictionary_value(command, key,
                                             actual_body_dictionary, expected_body[index]):
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


def validate_create_application(command, actual_body, expected_body):  # pylint: disable=too-many-return-statements
    """
    Validates that the input parameter for creating an application is correct.

    :param command: str - the command being run.

    :param expected_body: dictionary representing the expected body, containing the following items:

        name: str - the name of the application. This is the expected value
        type_name: str - application type name. This is the expected value
        type_version: str - application type version. This is the expected value
        parameters: list of list of ApplicationParameter objects represented as a tuple of
            [(str - key, str - value)]. This is the expected value
        min_nodes: int. This is the expected value
        max_nodes: int. This is the expected value
        application_metric_descriptions: list of ApplicationMetricDescription objects represented
            as a tuple of (str, int, int, int) containing
            (Name, MaximumCapacity, ReservationCapacity, TotalApplicationCapacity)
            This is the expected value

    :param actual_body: obj. The actual body that's passed in.

    :return: True if the actual body matches the expected. False otherwise.

    Sample actual body:

        {'Name': 'fabric:/application1',
        'TypeName': 'applicationType',
        'TypeVersion': '1',
        'ParameterList': [{'Key': 'Key', 'Value': 'Value'}],
        'ApplicationCapacity': {'MinimumNodes': 2, 'MaximumNodes': 3,
            'ApplicationMetrics': [{'Name': 'some_name',
                                    'MaximumCapacity': 5,
                                    'ReservationCapacity': 3,
                                    'TotalApplicationCapacity': 8}]}}
    """

    try:
        matching0 = _check_and_print_matching_error(command, 'application name',
                                                    actual_body['Name'], expected_body['Name'])

        matching1 = _check_and_print_matching_error(command, 'type name',
                                                    actual_body['TypeName'],
                                                    expected_body['TypeName'])

        matching2 = _check_and_print_matching_error(command, 'type version',
                                                    actual_body['TypeVersion'],
                                                    expected_body['TypeVersion'])

        matching3 = _check_and_print_matching_error(
            command, 'min nodes',
            actual_body['ApplicationCapacity']['MinimumNodes'],
            expected_body['MinNodes'])

        matching4 = _check_and_print_matching_error(
            command, 'max nodes',
            actual_body['ApplicationCapacity']['MaximumNodes'],
            expected_body['MaxNodes'])

        if not matching0 and matching1 and matching2 and matching3 and matching4:
            print('Application create body verify failed due to mismatched bodies', file=stderr)
            return False

        # Check the parameters
        expected_parameters = expected_body['ParameterList']
        actual_parameters_as_tuples = []
        for dict_item in actual_body['ParameterList']:
            actual_parameters_as_tuples.append(list(sorted(dict_item.items())))

        for tup in expected_parameters:  # example tup: [('Key', 'Key'), ('Value', 'Value')]
            if tup not in actual_parameters_as_tuples:
                print('Application create body verify failed due to missing expected '
                      'parameter set {0} from actual parameters list {1}'.format(
                          str(tup), str(actual_parameters_as_tuples)), file=stderr)
                return False

        if len(expected_parameters) != len(actual_parameters_as_tuples):
            print('Application create body verify failed due to mismatched '
                  'parameter set lengths. Actual: {0} Expected: {1}'.format(
                      str(len(expected_parameters)),
                      str(len(actual_parameters_as_tuples))), file=stderr)
            return False

        # Check the application metrics
        actual_metrics_as_tuples = []
        for dict_item in actual_body['ApplicationCapacity']['ApplicationMetrics']:
            actual_metrics_as_tuples.append(list(sorted(dict_item.items())))

        for tup in expected_body['ApplicationMetricDescriptions']:
            if tup not in actual_metrics_as_tuples:
                print('Application create body verify failed due to missing '
                      'metrics set {0} from actual list {1}'.format(str(tup),
                                                                    str(actual_metrics_as_tuples)),
                      file=stderr)
                return False

        if len(expected_body['ApplicationMetricDescriptions']) != \
                len(actual_metrics_as_tuples):
            print('Application create body verify failed due to mismatched '
                  'metics set lengths. Actual: {0} Expected: {1}'.format(
                      str(len(expected_body['ApplicationMetricDescriptions'])),
                      str(len(actual_metrics_as_tuples))), file=stderr)
            return False

    except KeyError as ex:
        print(
            'validation of {0} failed: Key not found. {1}'.format(
                command,
                str(ex)),
            file=stderr)
        return False

    return True
