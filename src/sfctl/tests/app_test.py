# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Custom app command tests"""

import unittest
import os
import json

try:
    from urllib import parse
except ImportError:
    import urlparse as parse
from mock import patch, MagicMock
import requests
import vcr
import sfctl.custom_app as sf_c
from sfctl.tests.mock_server import (find_localhost_free_port, start_mock_server)
from sfctl.custom_exceptions import SFCTLInternalException
from sfctl.tests.helpers import (MOCK_CONFIG, get_mock_endpoint, set_mock_endpoint)


class AppTests(unittest.TestCase):
    """App tests"""

    @classmethod
    def setUpClass(cls):
        """A class method called before tests in an individual class are run"""
        cls.port = find_localhost_free_port()
        cls.old_endpoint = get_mock_endpoint()

        # Start mock server
        start_mock_server(cls.port)

    @classmethod
    def tearDownClass(cls):
        """A class method called after tests in an individual class have run"""

        set_mock_endpoint(cls.old_endpoint)

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
        from azure.servicefabric.models import ApplicationParameter

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
        from azure.servicefabric.models import ApplicationMetricDescription

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


    def test_upload_image_store_timeout_overall(self):  #pylint: disable=invalid-name
        """
        Test to make sure that we end the overall upload process when it times out.

        Things we check for:
        - Where the timeout is not sufficient - too small for one file
            - Should get SFCTLInternalException
            - Manually make sure there is only one outgoing request with the correct timeout
              since it's hard to record the http request from another process.
        """

        # Doing patch here because patching outside of the function does not work
        with patch('sfctl.config.CLIConfig', new=MOCK_CONFIG):

            current_directory = os.path.dirname(os.path.realpath(__file__))
            # 4 files total in sample_nested_folders
            path_to_upload_file = os.path.join(current_directory, 'sample_nested_folders')
            endpoint = 'http://localhost:' + str(self.port)
            set_mock_endpoint(endpoint)

            # Mock server will take 3 seconds to respond to each request, simulating
            # a large file.

            exception_triggered = False
            try:
                timeout = 2
                sf_c.upload(path_to_upload_file, timeout=timeout)
            except SFCTLInternalException as ex:
                self.assertIn(
                    'Upload has timed out. Consider passing a longer timeout duration.',
                    ex.message,
                    msg='Application upload to image store returned the incorrect timeout message')
                exception_triggered = True
            # ConnectionResetError will be returned when the process cuts off, but we expect
            # upload to swallow that and return SFCTLInternalException

            self.assertTrue(exception_triggered, msg='A timeout exception is expected during '
                                                     'application upload timeout test with '
                                                     'response time 2 on the server side. '
                                                     'And timeout 2 overall.')

    def test_upload_image_store_timeout_long(self):  #pylint: disable=too-many-locals,invalid-name
        """Test function upload_to_native_imagestore to check that is it sending each
        file upload with the appropriate timeout. Does not look at overall timeout

        Things we check for:
        - Where the timeout is sufficient to completing the task.
            - Make sure the # of requests is correct -> # of files + # of dirs
            - Make sure that each URL shows a decreasing amount of time left"""

        current_directory = os.path.dirname(os.path.realpath(__file__))
        # 4 files total in sample_nested_folders
        path_to_upload_file = os.path.join(current_directory, 'sample_nested_folders')
        endpoint = 'http://localhost:' + str(self.port)
        basename = os.path.basename(path_to_upload_file)

        generated_file_path = 'native_image_store_upload_test.json'

        with requests.Session() as sesh:
            # Session does not need any security

            # Testing long timeout - expect upload completion

            # In case this file was created and not deleted by a previous test,
            # delete it here
            try:
                os.remove(generated_file_path)
            except OSError:
                # if the file doesn't exist, then there's nothing for us to do here
                pass

            timeout = 65  # upload should complete
            with vcr.use_cassette(generated_file_path, record_mode='all',
                                  serializer='json'), \
                 patch('sfctl.custom_app.get_job_count') as get_job_count_mock:

                get_job_count_mock.return_value = 1
                sf_c.upload_to_native_imagestore(sesh, endpoint, path_to_upload_file, basename,
                                                 show_progress=False, timeout=timeout)

        # Read in the json file to make sure that each file waited ~3 seconds, and not much more
        # or less.

        with open(generated_file_path, 'r') as http_recording_file:
            json_str = http_recording_file.read()
            vcr_recording = json.loads(json_str)

            requests_list = vcr_recording['interactions']
            self.assertEqual(len(requests_list), 8, msg='Application upload test: '
                                                        'An incorrect number of requests '
                                                        'was generated.')

            iteration = 0
            for request in requests_list:
                uri = request['request']['uri']
                parsed_url = parse.urlparse(uri)
                query = parse.parse_qs(parsed_url.query)
                query_timeout = query['timeout']

                # Here 3 is the response time in seconds from the mock server
                # however, the mock server can be a bit slow, taking an extra second from receiving
                # the request to start processing it. Linux does not seem to have this problem.
                # Issue seen on Windows only. If testing on windows, change the 3 seconds to 4.
                self.assertAlmostEqual(int(query_timeout[0]), timeout-iteration*3, delta=2)

                iteration += 1
