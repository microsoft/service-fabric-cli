# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Custom app command tests"""

import unittest
import os
import sfctl.custom_app as sf_c

class AppTests(unittest.TestCase):
    """App tests"""

    def app_path_absolute_test(self):
        """App path returns absolute path always"""
        import os
        import tempfile
        import shutil

        test_dir = tempfile.mkdtemp()
        self.addCleanup(lambda: shutil.rmtree(test_dir))

        res = sf_c.validate_app_path(test_dir)
        self.assertEqual(os.path.abspath(res), res)

    def app_path_file_error_test(self):
        """App path raise ValueError on non directory arguments"""
        import tempfile
        import os

        (test_fd, test_path) = tempfile.mkstemp()

        def cleanup():
            """Cleanup test files created"""
            os.close(test_fd)
            os.remove(test_path)

        self.addCleanup(cleanup)

        with self.assertRaises(ValueError):
            sf_c.validate_app_path(test_path)

    def parse_app_params_none_test(self):
        """Parse app params returns None with None args"""
        self.assertIs(sf_c.parse_app_params(None), None)

    def parse_app_params_empty_test(self):
        """Parse app params returns empty list with empty args"""
        self.assertEqual(sf_c.parse_app_params(""), [])

    def parse_single_app_param_test(self):
        """Parse app params returns a single parameter successfully"""
        from azure.servicefabric.models.application_parameter import (
            ApplicationParameter
        )

        res = sf_c.parse_app_params({'test': 'test2'})
        self.assertEqual(len(res), 1)
        res = res[0]
        self.assertIsInstance(res, ApplicationParameter)
        self.assertEqual(res.key, 'test')
        self.assertEqual(res.value, 'test2')

    def parse_app_metrics_none_test(self):
        """Parse app metrics returns None with None args"""
        self.assertIs(sf_c.parse_app_metrics(None), None)

    def parse_app_metrics_empty_test(self):
        """Parse app metrics returns empty list with empty args"""
        self.assertEqual(sf_c.parse_app_metrics(''), [])

    def parse_app_metrics_single_test(self):
        """Parse app metrics returns a single metric successfully"""
        from azure.servicefabric.models.application_metric_description import (
            ApplicationMetricDescription
        )

        res = sf_c.parse_app_metrics([{'name': 'test',
                                       'maximum_capacity': '3',
                                       'reservation_capacity': '2',
                                       'total_application_capacity': '2'}])
        self.assertEqual(len(res), 1)
        res = res[0]
        self.assertIsInstance(res, ApplicationMetricDescription)
        self.assertEqual(res.name, 'test')
        self.assertEqual(res.maximum_capacity, '3')
        self.assertEqual(res.reservation_capacity, '2')
        self.assertEqual(res.total_application_capacity, '2')

    def parse_cluster_manifest_test(self):
        """Parse cluster manifest loaded from a file"""
        filepath = os.path.normpath(
            os.path.join(
                os.path.dirname(
                    os.path.realpath(__file__)),
                'clustermanifest1.txt'))
        f = open(filepath, 'r')
        content = f.read()
        f.close()
        self.assertEqual(sf_c.parse_imagestore_connection_string(content),
                         'fabric:ImageStore')

    def parse_empty_cluster_manifest_test(self): #pylint: disable=invalid-name
        """Parse empty cluster manifest content"""
        self.assertEqual(sf_c.parse_imagestore_connection_string(None),
                         None)

    def parse_missing_imagestore_entry_cluster_manifest_test(self): #pylint: disable=invalid-name
        """Parse missing image store connection string in cluster manifest"""
        filepath = os.path.normpath(
            os.path.join(
                os.path.dirname(
                    os.path.realpath(__file__)),
                'invalid_clustermanifest1.txt'))
        f = open(filepath, 'r')
        content = f.read()
        f.close()
        self.assertEqual(sf_c.parse_imagestore_connection_string(content),
                         None)

    def parse_invalid_cluster_manifest_test(self): #pylint: disable=invalid-name
        """Parse invalid cluster manifest loaded from a file"""
        filepath = os.path.normpath(
            os.path.join(
                os.path.dirname(
                    os.path.realpath(__file__)),
                'invalid_clustermanifest2.txt'))
        f = open(filepath, 'r')
        content = f.read()
        f.close()
        self.assertEqual(sf_c.parse_imagestore_connection_string(content),
                         None)

    def parse_fileshare_path_test(self):
        """Parse fileshare path from the cluster manifest"""
        filepath = os.path.normpath(
            os.path.join(
                os.path.dirname(
                    os.path.realpath(__file__)),
                'clustermanifest2.txt'))
        f = open(filepath, 'r')
        content = f.read()
        f.close()
        self.assertEqual(sf_c.parse_imagestore_connection_string(content),
                         'file:C:\\temp')
        self.assertEqual(sf_c.parse_file_share_path(
            sf_c.parse_imagestore_connection_string(content)), 'C:\\temp')

    def upload_to_fileshare_test(self):
        """Uploads the package to the fileshare"""
        import tempfile
        import shutil
        try:
            src_dir = os.path.dirname(os.path.realpath(__file__))
            fileshare_dir = tempfile.mkdtemp()
            sf_c.upload_to_fileshare(src_dir, fileshare_dir, False)
            src_files_count = 0
            fileshare_files_count = 0
            for _, _, files in os.walk(src_dir):
                src_files_count += (len(files) + 1)
            for _, _, files in os.walk(fileshare_dir):
                fileshare_files_count += (len(files) + 1)
            #account for _.dir in the dest directory
            self.assertEqual(src_files_count + 1, fileshare_files_count)
        finally:
            shutil.rmtree(fileshare_dir)
