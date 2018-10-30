# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Custom mesh command tests"""

import unittest
import json
import os
import shutil
from knack.util import CLIError
from sfmergeutility import SFMergeUtility
import sfctl.custom_deployment as sf_r
from sfctl.custom_deployment import ResourceType

class MeshTests(unittest.TestCase):
    """Mesh command tests """

    def get_actual_json_file(self, actual_json_files, generated_json_file):
        """Gets the actual json file w.r.t the generated json file"""
        resource_name = sf_r.get_resource_name(generated_json_file)
        generated_resource_type = sf_r.get_resource_type(generated_json_file)
        return_file = None
        for actual_json_file in actual_json_files:
            actual_resource_type = sf_r.get_resource_type(actual_json_file)
            if resource_name in actual_json_file and generated_resource_type == actual_resource_type: # pylint: disable=line-too-long
                return_file = actual_json_file
                break
        self.assertNotEqual(return_file, None)
        return return_file

    def test_merge_utility(self):
        """Test merge utility if it is generating the correct jsons"""
        sample_json_path = os.path.join(os.path.dirname(__file__), 'sample_json')
        sample_yaml_path = os.path.join(os.path.dirname(__file__), 'sample_yaml')
        yaml_file_path_list = sf_r.list_files_directory(sample_yaml_path, ".yaml")
        output_dir = os.path.join(os.path.dirname(__file__), "meshDeploy")
        SFMergeUtility.sf_merge_utility(yaml_file_path_list, "SF_SBZ_JSON", parameter_file=None, output_dir=output_dir, prefix="resource", region="westus") # pylint: disable=line-too-long
        generated_json_files = sf_r.list_files_directory(output_dir, ".json")
        actual_json_files = sf_r.list_files_directory(sample_json_path, ".json")
        for generated_json_file in generated_json_files:
            generated_json_file_fp = open(generated_json_file, "r")
            generated_json = json.load(generated_json_file_fp)
            generated_json_file_fp.close()
            actual_json_file = self.get_actual_json_file(actual_json_files, generated_json_file)
            actual_json_file_fp = open(actual_json_file, "r")
            actual_json = json.load(actual_json_file_fp)
            actual_json_file_fp.close()
            self.assertEqual(generated_json, actual_json)
        shutil.rmtree(output_dir, ignore_errors=True)

    def test_resource_type(self):
        """Test resource type is correctly identified or not"""
        resource_type = sf_r.get_resource_type("merged-0006_application_counterApp-AZFiles.json")
        self.assertEqual(resource_type, ResourceType.application)
        resource_type = sf_r.get_resource_type("merged-0001_secret_azurefilesecret.json")
        self.assertEqual(resource_type, ResourceType.secret)
        resource_type = sf_r.get_resource_type("merged-0002_secretValue_azurefilesecret_v1.json")
        self.assertEqual(resource_type, ResourceType.secretValue)
        resource_type = sf_r.get_resource_type("merged-0003_volume_counterVolumeWindows.json")
        self.assertEqual(resource_type, ResourceType.volume)
        resource_type = sf_r.get_resource_type("merged-0004_network_counterAppNetwork.json")
        self.assertEqual(resource_type, ResourceType.network)
        resource_type = sf_r.get_resource_type("merged-0005_gateway_counterAppGateway.json")
        self.assertEqual(resource_type, ResourceType.gateway)
        resource_type = sf_r.get_resource_type("merged-0005_something_counterAppGateway.json")
        self.assertEqual(resource_type, None)
        with self.assertRaises(CLIError):
            resource_type = sf_r.get_resource_type("invalid-file-name.json")

    def test_mesh_deploy_invalid(self):
        """ Test to check if mesh deployment command fails when invalid path is provided"""
        with self.assertRaises(CLIError):
            sf_r.mesh_deploy(None, "some-dummy-file-path")

    def test_resource_name(self):
        """Test resource name is correctly identified or not"""
        resource_name = sf_r.get_resource_name("merged-0006_application_counterApp-AZFiles.json")
        self.assertEqual("counterApp-AZFiles", resource_name)
        with self.assertRaises(CLIError):
            resource_name = sf_r.get_resource_type("invalid-file-name.json")

def ordered_json(json_dict):
    """Creates a ordered json for comparison"""
    if isinstance(json_dict, dict):
        return sorted((k, ordered_json(v)) for k, v in json_dict.items())
    if isinstance(json_dict, list):
        return sorted(ordered_json(x) for x in json_dict)
    return json_dict
