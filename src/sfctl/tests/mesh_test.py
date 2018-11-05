# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Custom mesh command tests"""

import unittest
from knack.util import CLIError
import sfctl.custom_deployment as sf_resource
from sfctl.custom_deployment import ResourceType

class MeshTests(unittest.TestCase):
    """Mesh command tests """

    def test_resource_type(self):
        """Test if resource type is correctly identified or not"""
        resource_type = sf_resource.get_resource_type("merged-0006_application_counterApp-AZFiles.json")  # pylint: disable=line-too-long
        self.assertEqual(resource_type, ResourceType.application)
        resource_type = sf_resource.get_resource_type("merged-0001_secret_azurefilesecret.json")
        self.assertEqual(resource_type, ResourceType.secret)
        resource_type = sf_resource.get_resource_type("merged-0002_secretValue_azurefilesecret_v1.json")  # pylint: disable=line-too-long
        self.assertEqual(resource_type, ResourceType.secretValue)
        resource_type = sf_resource.get_resource_type("merged-0003_volume_counterVolumeWindows.json")  # pylint: disable=line-too-long
        self.assertEqual(resource_type, ResourceType.volume)
        resource_type = sf_resource.get_resource_type("merged-0004_network_counterAppNetwork.json")
        self.assertEqual(resource_type, ResourceType.network)
        resource_type = sf_resource.get_resource_type("merged-0005_gateway_counterAppGateway.json")
        self.assertEqual(resource_type, ResourceType.gateway)
        with self.assertRaises(CLIError):
            resource_type = sf_resource.get_resource_type("merged-0005_something_counterAppGateway.json")  # pylint: disable=line-too-long
        with self.assertRaises(CLIError):
            resource_type = sf_resource.get_resource_type("invalid-file-name.json")

    def test_mesh_deploy_invalid(self):
        """ Test to check if mesh deployment command fails when invalid path is provided"""
        with self.assertRaises(CLIError):
            sf_resource.mesh_deploy(None, "some-dummy-file-path")
        with self.assertRaises(CLIError):
            sf_resource.mesh_deploy(None, "some-dummy-file-path,another-dummy-file-path")

    def test_resource_name(self):
        """Test if resource name is correctly identified or not"""
        resource_name = sf_resource.get_resource_name("merged-0006_application_counterApp-AZFiles.json")  # pylint: disable=line-too-long
        self.assertEqual("counterApp-AZFiles", resource_name)
        with self.assertRaises(CLIError):
            resource_name = sf_resource.get_resource_type("invalid-file-name.json")
