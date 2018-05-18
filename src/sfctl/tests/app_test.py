# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Custom app command tests"""

import unittest
import os
from mock import patch, MagicMock
import sfctl.custom_app as sf_c


class AppTests(unittest.TestCase):
    """App tests"""

    def test_app_path_absolute(self):
        """App path returns absolute path always"""
        import tempfile
        import shutil

        test_dir = tempfile.mkdtemp()
        self.addCleanup(lambda: shutil.rmtree(test_dir))

        res = sf_c.validate_app_path(test_dir)
        self.assertEqual(os.path.abspath(res), res)

    def test_app_path_file_error(self):
        """App path raise ValueError on non directory arguments"""
        import tempfile

        (test_fd, test_path) = tempfile.mkstemp()

        def cleanup():
            """Cleanup test files created"""
            os.close(test_fd)
            os.remove(test_path)

        self.addCleanup(cleanup)

        with self.assertRaises(ValueError):
            sf_c.validate_app_path(test_path)

    def test_parse_app_params_none(self):
        """Parse app params returns None with None args"""
        self.assertIs(sf_c.parse_app_params(None), None)

    def test_parse_app_params_empty(self):
        """Parse app params returns empty list with empty args"""
        self.assertEqual(sf_c.parse_app_params(""), [])

    def test_parse_single_app_param(self):
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

    def test_parse_app_metrics_none(self):
        """Parse app metrics returns None with None args"""
        self.assertIs(sf_c.parse_app_metrics(None), None)

    def test_parse_app_metrics_empty(self):
        """Parse app metrics returns empty list with empty args"""
        self.assertEqual(sf_c.parse_app_metrics(''), [])

    def test_parse_app_metrics_single(self):
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

    def test_parse_fileshare_path(self):
        """Parse fileshare path from the image store connection string"""
        test_string = r'file:C:\test_store'
        expected_string = r'C:\test_store'
        self.assertEqual(sf_c.path_from_imagestore_string(test_string),
                         expected_string)

    def test_upload_to_fileshare(self):  # pylint: disable=no-self-use
        """Upload copies files to non-native store correctly with no
        progress"""
        import shutil
        import tempfile
        temp_file = tempfile.NamedTemporaryFile(dir=tempfile.mkdtemp())
        temp_src_dir = os.path.dirname(temp_file.name)
        temp_dst_dir = tempfile.mkdtemp()
        shutil_mock = MagicMock()
        shutil_mock.copyfile.return_value = None
        with patch('sfctl.custom_app.shutil', new=shutil_mock):
            sf_c.upload_to_fileshare(temp_src_dir, temp_dst_dir, False)
            shutil_mock.copyfile.assert_called_once()
        temp_file.close()
        shutil.rmtree(os.path.dirname(temp_file.name))
        shutil.rmtree(temp_dst_dir)
