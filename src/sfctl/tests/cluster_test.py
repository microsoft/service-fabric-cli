# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Custom cluster command tests"""

import unittest
from datetime import datetime
from knack.util import CLIError
from knack.testsdk import ScenarioTest
from mock import patch
import sfctl.custom_cluster as sf_c
from sfctl.tests.helpers import (MOCK_CONFIG, get_mock_endpoint, set_mock_endpoint)
from sfctl.entry import cli
from sfctl.custom_cluster import check_cluster_version, sfctl_cluster_version_matches
from sfctl.custom_exceptions import SFCTLInternalException
from sfctl import state as sfctl_state


class ClusterTests(unittest.TestCase):
    """Cluster tests"""

    def test_select_bad_ca_args(self):
        """Select with CA certs but not client certs returns error"""
        with self.assertRaises(CLIError):
            sf_c.select_arg_verify('http://test.com:190800', None, None, None,
                                   'ca_bundle', False, False)

    def test_select_missing_key_args(self):
        """Select with only cert file but not key returns error"""
        with self.assertRaises(CLIError):
            sf_c.select_arg_verify('http://test.com:190800', 'test.crt', None,
                                   None, None, False, False)

    def test_select_verify_missing_cert(self):
        """Select with no-verify but no cert returns error"""
        with self.assertRaises(CLIError):
            sf_c.select_arg_verify('http://test.com:190800', None, None, None,
                                   None, False, True)

    def test_select_two_cert_args(self):
        """Select with both cert and pem returns error"""
        with self.assertRaises(CLIError):
            sf_c.select_arg_verify('http://test.com:190800', 'test.crt',
                                   'test.key', 'test.pem', None, False, False)

    def test_select_cert_and_aad(self):
        """Select with both cert and aad returns error"""
        with self.assertRaises(CLIError):
            sf_c.select_arg_verify('http://test.com:190800', 'test.crt',
                                   'test.key', None, None, True, False)

    def test_sfctl_cluster_version_matches(self):  # pylint: disable=invalid-name
        """
        Test that the latest version of sfctl has a corresponding service fabric cluster
        version that it matches with.
        """
        current_sfctl_version = sfctl_state.get_sfctl_version()

        # An exception will be raised if the current cluster version doesn't exist in the function
        try:
            self.assertTrue(sfctl_cluster_version_matches('8.0', current_sfctl_version),
                            msg='You are most likely getting this error because we need to '
                                'update the method sfctl_cluster_version_matches in '
                                'custom_cluster so that it works with the '
                                'current version of sfctl, or we need to update this test.')
        except SFCTLInternalException as ex:
            # Give a more test appropriate error message
            self.fail(ex.message + ' You are most likely getting this error because we need to '
                                   'update the method sfctl_cluster_version_matches in '
                                   'custom_cluster so that it works with the '
                                   'current version of sfctl, or we need to update this test.')

    def test_version_check_older_cluster(self):  # pylint: disable=invalid-name
        """
        Test that when hitting an older cluster without a cluster version, the time is updated and
        we mark the cluster check as passed/not done.

        We don't actually hit a live cluster, so we will enter a dummy value of None to the
        function call, which is what the result will be http gateway returns error.
        """

        state_file_path = sfctl_state.get_state_path()

        # empty the file
        open(state_file_path, 'w').close()

        current_utc_time = datetime.utcnow()

        # Check cluster version. This should update the last updated time (in state)
        checks_passed_or_not_done = check_cluster_version(
            False, dummy_cluster_version='NoResult')

        self.assertTrue(checks_passed_or_not_done, 'check_cluster_version should return True '
                                                   'because checks should not be performed, '
                                                   'since we are simulating that we are a newer '
                                                   'sfctl hitting a cluster without the '
                                                   'get cluster version API.')

        self.assertGreater(sfctl_state.get_cluster_version_check_time(), current_utc_time,
                           'check_cluster_version command should have modified the '
                           'last checked time such that the time in state is greater than our '
                           'time.')


    def test_version_check_triggered(self):
        """Test that under the following circumstances, a cluster version & sfctl version
        compatibility check is triggered and verify that the last check time was left
        in a good state after the call:
            - The last check time (in state) doesn't exist yet
            - An error has occurred during function call
            - On connection to a new cluster even
                if time since last check is less than SF_CLI_VERSION_CHECK_INTERVAL
            - The last check time (in state) was greater than
                config.py's SF_CLI_VERSION_CHECK_INTERVAL

        NOTE: this is a unit test only, which relies on the
        custom_cluster.py - check_cluster_version
        function being called with the correct parameters, and being called at all.
        """

        # Start session state with condition last check time does not exist:
        state_file_path = sfctl_state.get_state_path()
        # If anything other than one line with our state exists in the file
        # (2 lines total - one to specify the section)
        # then throw an error. This may happen if sfctl uses the state file for something else.
        # If the state file ends up being used for anything else
        # other than last checked API version time, then modify this test then to remove
        # only that one line.
        with open(state_file_path) as state_file:
            content = state_file.readlines()

        content_trimmed = []
        for line in content:
            if line.strip():
                content_trimmed.append(line)

        self.assertLess(len(content_trimmed), 3,
                        'sfctl state file should not have more than 2 lines. '
                        'Content: ' + str(content_trimmed))

        # empty the file
        open(state_file_path, 'w').close()

        # Create cluster version object.
        cluster_version = 'invalid_version'

        current_utc_time = datetime.utcnow()

        # Check cluster version. This should update the last updated time (in state)
        checks_passed_or_not_done = check_cluster_version(
            False, dummy_cluster_version=cluster_version)

        self.assertFalse(checks_passed_or_not_done, 'check_cluster_version should return False '
                                                    'because checks were performed and the '
                                                    'versions do not match')
        self.assertGreater(sfctl_state.get_cluster_version_check_time(),
                           current_utc_time,
                           'check_cluster_version command should have modified the '
                           'last checked time such that the time in state is greater than our '
                           'time.')

        # Set the last checked time in state to something recent, and set calling on failure
        # to True
        sfctl_state.set_cluster_version_check_time(current_utc_time)

        checks_passed_or_not_done = check_cluster_version(
            on_failure_or_connection=True, dummy_cluster_version=cluster_version)

        self.assertFalse(checks_passed_or_not_done, 'check_cluster_version should return False '
                                                    'because checks were performed and the '
                                                    'versions do not match')
        self.assertGreater(sfctl_state.get_cluster_version_check_time(), current_utc_time,
                           'check_cluster_version command should have modified the '
                           'last checked time such that the time in state is greater than our '
                           'time.')

        # Last check time is in the past (well past SF_CLI_VERSION_CHECK_INTERVAL),
        # so should trigger an update and a check
        utc_time_past = datetime(
            year=current_utc_time.year - 1,
            month=12,
            day=20,
            hour=0,
            minute=0,
            second=0
        )

        sfctl_state.set_cluster_version_check_time(utc_time_past)

        checks_passed_or_not_done = check_cluster_version(
            on_failure_or_connection=False, dummy_cluster_version=cluster_version)

        self.assertFalse(checks_passed_or_not_done, 'check_cluster_version should return False '
                                                    'because checks were performed and the '
                                                    'versions do not match')
        self.assertGreater(sfctl_state.get_cluster_version_check_time(), utc_time_past,
                           'check_cluster_version command should have modified the '
                           'last checked time such that the time in state is greater than our '
                           'time.')

    def test_version_check_not_triggered(self):  # pylint: disable=invalid-name
        """Test that under the following circumstances, a cluster version & sfctl version
        compatibility check is NOT triggered and if the last check time was left in a good state
        after the call:
            - The last check time was less than config.py - SF_CLI_VERSION_CHECK_INTERVAL

        NOTE: this is a unit test only, which relies on the
        custom_cluster.py - check_cluster_version
        function being called with the correct parameters, and being called at all.

        This test assumes SF_CLI_VERSION_CHECK_INTERVAL = 24 hours
        """

        current_utc_time = datetime.utcnow()

        adjusted_hour = current_utc_time.hour
        adjusted_minute = current_utc_time.minute
        adjusted_day = current_utc_time.day
        if adjusted_minute >= 5:
            adjusted_minute = adjusted_minute - 5
        elif adjusted_hour >= 1:
            adjusted_hour = adjusted_hour - 1
        else:
            adjusted_day = adjusted_day- 1
            adjusted_hour = 23

        utc_time_past = datetime(
            year=current_utc_time.year,
            month=current_utc_time.month,
            day=adjusted_day,
            hour=adjusted_hour,
            minute=adjusted_minute
        )

        cluster_version = 'invalid_version'

        # Configure last checked time to current time minus some amount of time less than 24 hours
        # Run check_cluster_version
        # Check that the values in the state file of the last checked time is correct
        # Test may fail if SF_CLI_VERSION_CHECK_INTERVAL value is too low.

        sfctl_state.set_cluster_version_check_time(utc_time_past)
        checks_passed_or_not_done = check_cluster_version(
            on_failure_or_connection=False, dummy_cluster_version=cluster_version)

        self.assertTrue(checks_passed_or_not_done, 'check_cluster_version should return True '
                                                   'because no checks were performed')
        self.assertEqual(utc_time_past, sfctl_state.get_cluster_version_check_time(),
                         'check_cluster_version command should not have modified the '
                         'last checked time values since it should have returned True, having '
                         'done no work.')

        # Configure last checked time to current time
        # Run check_cluster_version
        # Check that the values in the state file of the last checked time is correct

        current_utc_time = datetime.utcnow()
        sfctl_state.set_cluster_version_check_time(current_utc_time)

        checks_passed_or_not_done = check_cluster_version(
            on_failure_or_connection=False, dummy_cluster_version=cluster_version)

        self.assertTrue(checks_passed_or_not_done, 'check_cluster_version should return True '
                                                   'because no checks were performed')
        self.assertEqual(current_utc_time, sfctl_state.get_cluster_version_check_time(),
                         'check_cluster_version command should not have modified the '
                         'last checked time values since it should have returned True, having '
                         'done no work.')


class ClusterScenarioTests(ScenarioTest):
    """Cluster scenario tests"""

    def __init__(self, method_name):
        cli_env = cli()
        super(ClusterScenarioTests, self).__init__(cli_env, method_name)

    @patch('sfctl.config.CLIConfig', new=MOCK_CONFIG)
    def test_show_cluster(self):
        """Ensure that the correct message is returned when a cluster is set"""
        old_endpoint = get_mock_endpoint()

        set_mock_endpoint('https://testUrl.com')

        self.assertEqual('https://testUrl.com', sf_c.show_connection())

        set_mock_endpoint(str(old_endpoint))

    @patch('sfctl.config.CLIConfig', new=MOCK_CONFIG)
    def test_show_cluster_no_endpoint(self):
        """Ensure that the correct message is returned when a cluster is not set"""
        old_endpoint = get_mock_endpoint()

        set_mock_endpoint('')

        self.assertEqual(None, sf_c.show_connection())

        set_mock_endpoint(str(old_endpoint))
