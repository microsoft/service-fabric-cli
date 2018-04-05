# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Custom cluster command tests"""

import unittest
from knack.util import CLIError
import sfctl.custom_cluster as sf_c


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
