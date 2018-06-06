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
        target_sf_version = '6.2.0.0'
        correct_output = '{0} with target service Fabric version of {1}'.format(sfctl_version, target_sf_version)

        # Call the provided command in command line
        # Do not split the help_command, as that breaks behavior:
        # Linux ignores the splits and takes only the first.
        pipe = Popen('sfctl version', shell=True, stdout=PIPE, stderr=PIPE)
        # returned_string and err are returned as bytes
        (returned_string, err) = pipe.communicate()

        returned_string = returned_string.decode('utf-8').strip()

        self.assertEqual(returned_string, correct_output)
