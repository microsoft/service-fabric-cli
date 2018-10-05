# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Custom app command tests"""

import unittest
import os
from mock import patch, MagicMock
import requests
import vcr
from jsonpickle import decode
import sfctl.custom_app as sf_c
from sfctl.tests.mock_server import (find_localhost_free_port, start_mock_server)
from sfctl.custom_exceptions import SFCTLInternalException
from sfctl.tests.helpers import (MOCK_CONFIG, get_mock_endpoint, set_mock_endpoint, ENDPOINT)


class AppTests(unittest.TestCase):
    """App tests"""

    @classmethod
    def setUpClass(self):
        """A class method called before tests in an individual class are run"""
        # self.old_endpoint = get_mock_endpoint()
        self.port = find_localhost_free_port()
        self.old_endpoint = get_mock_endpoint()

        # Start mock server
        start_mock_server(self.port)

    @classmethod
    def tearDownClass(self):
        """A class method called after tests in an individual class have run"""

        set_mock_endpoint(self.old_endpoint)

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

    # @patch('sfctl.config.CLIConfig', new=MOCK_CONFIG)
    def test_upload_to_native_image_store_timeout_overall(self):
        """
        Test to make sure that we end the overall upload process when it times out
        """

        # Doing patch here because patching outside of the function does not work
        with patch('sfctl.config.CLIConfig', new=MOCK_CONFIG):

            current_directory = os.path.dirname(os.path.realpath(__file__))
            # 4 files total in sample_nested_folders
            path_to_upload_file = os.path.join(current_directory, 'sample_nested_folders')
            endpoint = 'http://localhost:' + str(self.port)
            set_mock_endpoint(endpoint)

            generated_file_path = 'native_image_store_upload_test.json'

            with requests.Session() as sesh:
                # Session does not need any security

                print('--------------------------------')
                print('Testing shot timeout - 2 seconds')
                print('--------------------------------')

                exception_triggered = False
                try:
                    timeout = 3  # Timeout set to 60 seconds.
                    sf_c.upload(path_to_upload_file, timeout=timeout)
                except SFCTLInternalException as e:
                    self.assertIn(
                        'Upload has timed out. Consider passing a longer timeout duration.',
                        e.message,
                        msg='Application upload to image store returned the incorrect timeout message')
                    exception_triggered = True
                except ConnectionResetError:
                    pass  # this will be returned when the process cuts off

                self.assertTrue(exception_triggered, msg='A timeout exception is expected during '
                                                         'application upload timeout test with '
                                                         'timeout 5 on the server side. And timeout '
                                                         '5 overall.')

                import time
                time.sleep(15)

                print('--------------------------------')
                print('Testing should timeout - 12 seconds')
                print('--------------------------------')

                # In case this file was created and not deleted by a previous test,
                # delete it here
                try:
                    os.remove(generated_file_path)
                except OSError:
                    # if the file doesn't exist, then there's nothing for us to do here
                    pass

                try:
                    timeout = 12  # upload should not finish
                    with vcr.use_cassette(generated_file_path, record_mode='all',
                                          serializer='json'):
                        sf_c.upload(path_to_upload_file, timeout=timeout)
                except Exception as e:
                    exception_triggered = True

                self.assertTrue(exception_triggered, msg='An exception is not expected during '
                                                          'application upload timeout test with '
                                                          'timeout 12 overall')

                with open(generated_file_path, 'r') as http_recording_file:
                    json_str = http_recording_file.read()
                    vcr_recording = decode(json_str)

                    # The responses create an array of request and other objects.
                    # the numbers (for indexing) represent which request was made
                    # first. The ordering is determined by the ordering of calls to self.cmd.
                    # see outputted JSON file at generated_file_path for more details.
                    recording = vcr_recording['interactions'][0]['request']

            # Read in the json file to make sure that each file waited ~5 seconds, and not much more
            # or less.

    # @patch('sfctl.config.CLIConfig', new=MOCK_CONFIG)
    def test_upload_to_native_image_store_timeout_single(self):
        """Test function upload_to_native_imagestore to check that is it sending each
        file upload with the appropriate timeout. Does not look at overall timeout"""

        current_directory = os.path.dirname(os.path.realpath(__file__))
        # 4 files total in sample_nested_folders
        path_to_upload_file = os.path.join(current_directory, 'sample_nested_folders')
        endpoint = 'http://localhost:' + str(self.port)
        basename = os.path.basename(path_to_upload_file)

        generated_file_path = 'native_image_store_upload_test.json'

        with requests.Session() as sesh:
            # Session does not need any security

            print('-----------------------------------------------')
            print('Testing long timeout - expect upload completion')
            print('-----------------------------------------------')

            # In case this file was created and not deleted by a previous test,
            # delete it here
            try:
                os.remove(generated_file_path)
            except OSError:
                # if the file doesn't exist, then there's nothing for us to do here
                pass

            timeout = 60  # upload should complete
            with vcr.use_cassette(generated_file_path, record_mode='all',
                                  serializer='json'):

                sf_c.upload(path_to_upload_file, timeout=timeout)

            # Read in the json file to make sure that each file waited ~5 seconds, and not much more
            # or less.




