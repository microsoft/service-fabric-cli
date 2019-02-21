# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""A mock server for testing purposes."""

from threading import Thread
import socket
try:
    from urllib import parse
except ImportError:
    import urlparse as parse
from future.backports.http.server import (BaseHTTPRequestHandler, HTTPServer)
import requests


class MockServer(BaseHTTPRequestHandler):
    """ Overrides the following methods in BaseHTTPRequestHandler """

    # pylint: disable=no-member

    def do_GET(self):  # pylint: disable=C0103,missing-docstring
        self.send_response(requests.codes.ok)
        self.end_headers()

    def do_PUSH(self):  # pylint: disable=C0103,missing-docstring
        self.send_response(requests.codes.ok)
        self.end_headers()

    def do_POST(self):  # pylint: disable=C0103,missing-docstring
        # Certain requests expect a very specific response.
        # For those, return other status codes
        if (self.path.startswith('/$/RollbackUpgrade?') or
                self.path.startswith('/ComposeDeployments/deploymentName/$/Delete') or
                self.path.startswith('/$/StartClusterConfigurationUpgrade')):
            self.send_response(requests.codes.accepted)
            self.end_headers()
            return

        if self.path.startswith('/Applications/$/Create'):
            self.send_response(requests.codes.created)
            self.end_headers()
            return

        # Return ok as the default response
        self.send_response(requests.codes.ok)
        self.end_headers()

    def do_PUT(self):  # pylint: disable=C0103,missing-docstring
        # Return 200 as the default response

        if self.path.startswith('/ImageStore/') and self.path.find('sample_nested_folders') != -1:

            parsed_url = parse.urlparse(self.path)
            query = parse.parse_qs(parsed_url.query)  # This is a dict of lists

            counter = 0
            import time

            while int(query['timeout'][0]) > 0 and counter < 3:
                time.sleep(1)
                counter += 1

        self.send_response(requests.codes.ok)
        self.end_headers()

    def do_DELETE(self):  # pylint: disable=C0103,missing-docstring
        # Return 200 as the default response
        self.send_response(requests.codes.ok)
        self.end_headers()


def find_localhost_free_port():
    """ Return a free port. """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # binds to 0, which auto reassigns to a free port
    sock.bind(('localhost', 0))

    # using [1] to access returned pair of address, port
    return sock.getsockname()[1]


def start_mock_server(port):
    """ Start a new mock server at localhost:port. """
    mock_server = HTTPServer(('localhost', port), MockServer)
    mock_server_thread = Thread(target=mock_server.serve_forever)
    mock_server_thread.setDaemon(True)  # Set automatic cleanup of this thread
    mock_server_thread.start()
