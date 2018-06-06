# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Custom cluster command tests"""

import unittest
from knack.util import CLIError
from knack.testsdk import ScenarioTest
from mock import patch
import sfctl.custom_cluster as sf_c
from sfctl.tests.helpers import (MOCK_CONFIG, get_mock_endpoint, set_mock_endpoint)
from sfctl.entry import cli


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
