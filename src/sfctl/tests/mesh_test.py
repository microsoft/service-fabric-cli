# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Custom mesh command tests"""

import unittest
from knack.util import CLIError
import sfctl.custom_deployment as sf_resource

class MeshTests(unittest.TestCase):
    """Mesh command tests """

    def test_mesh_deploy_invalid(self):
        """ Test to check if mesh deployment command fails when invalid path is provided"""
        with self.assertRaises(CLIError):
            sf_resource.mesh_deploy(None, "some-dummy-file-path")
        with self.assertRaises(CLIError):
            sf_resource.mesh_deploy(None, "some-dummy-file-path,another-dummy-file-path")
