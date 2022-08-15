# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""version command tests"""
import unittest
from subprocess import Popen, PIPE

class VersionTests(unittest.TestCase):
    """Verify current sfctl version"""

    def test_valid_current_version(self):
        """Tests that --version does not return error and includes the version.

        note: this will require changing the sfctl_version on releases
        """
        sfctl_version = '11.2.0'

        pipe = Popen('sfctl --version', shell=True, stdout=PIPE, stderr=PIPE)
        # returned_string and err are returned as bytes
        (returned_string, err) = pipe.communicate()

        if err:
            err = err.decode('utf-8')
            self.fail(msg='ERROR: version command returning with error : {0}'.format(err))

        returned_strings = returned_string.decode('utf-8').splitlines()
        returned_string = returned_strings[0].strip()

        self.assertEqual(returned_string, sfctl_version)
