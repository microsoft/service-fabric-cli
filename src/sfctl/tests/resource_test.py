# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Custom application resource model command tests"""

import unittest
from os import path
import sfctl.custom_resource as sf_r
from sfctl.custom_resource import ResourceType

class ResourceTests(unittest.TestCase):
    """Application resource model tests"""
    sample_yaml_path = path.join(path.dirname(__file__), 'sample_yaml')

    def check_valid_application_resource(self): #pylint: disable=invalid-name
        """Checks the application resource yaml is correctly identified"""
        sample_application_yaml_path = path.join(self.sample_yaml_path, 'sample_app.yaml')
        r_val = sf_r.get_valid_resource_type(sample_application_yaml_path,
                                             sf_r.get_yaml_content(sample_application_yaml_path))
        self.assertEqual(r_val, ResourceType.application)

    def check_valid_service_resource(self): #pylint: disable=invalid-name
        """Checks the service resource yaml is correctly identified"""
        sample_service_yaml_path = path.join(self.sample_yaml_path, 'sample_service.yaml')
        r_val = sf_r.get_valid_resource_type(sample_service_yaml_path,
                                             sf_r.get_yaml_content(sample_service_yaml_path))
        self.assertEqual(r_val, ResourceType.service)

    def check_valid_volume_resource(self): #pylint: disable=invalid-name
        """Checks the service resource yaml is correctly identified"""
        sample_volume_yaml_path = path.join(self.sample_yaml_path, 'sample_service.yaml')
        r_val = sf_r.get_valid_resource_type(sample_volume_yaml_path,
                                             sf_r.get_yaml_content(sample_volume_yaml_path))
        self.assertEqual(r_val, ResourceType.volume)
        