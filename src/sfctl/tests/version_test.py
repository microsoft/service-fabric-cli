# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Custom service command tests"""
import unittest
from subprocess import Popen, PIPE

class VersionTests(unittest.TestCase):
    def test_valid_current_version(self):
        sfctl_version = '5.0.0'

        pipe = Popen('sfctl --version', shell=True, stdout=PIPE, stderr=PIPE)
        # returned_string and err are returned as bytes
        (returned_string, err) = pipe.communicate()

        returned_strings = returned_string.decode('utf-8').splitlines()
        returned_string = returned_strings[0].strip()

        self.assertEqual(returned_string, sfctl_version)
