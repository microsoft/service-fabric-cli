# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""A mock server for testing purposes."""

from threading import Thread
import socket
from future.backports.http.server import (BaseHTTPRequestHandler, HTTPServer)
import requests


class MockServer(BaseHTTPRequestHandler):
    """ Overrides the following methods in BaseHTTPRequestHandler """

    # pylint: disable=no-member

    def do_GET(self):  # pylint: disable=C0103,missing-docstring
        self.send_response(requests.codes.ok)
        self.end_headers()
        return

    def do_PUSH(self):  # pylint: disable=C0103,missing-docstring
        self.send_response(requests.codes.ok)
        self.end_headers()
        return

    def do_POST(self):  # pylint: disable=C0103,missing-docstring
        # Certain requests expect a very specific response.
        # For those, return other status codes
        if self.path.startswith('/$/RollbackUpgrade?') or self.path.startswith('/ComposeDeployments/deploymentName/$/Delete'):  # pylint: disable=line-too-long
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
        return

    def do_PUT(self):  # pylint: disable=C0103,missing-docstring
        # Return 200 as the default response
        self.send_response(requests.codes.ok)
        self.end_headers()
        return

    def do_DELETE(self):  # pylint: disable=C0103,missing-docstring
        # Return 200 as the default response
        self.send_response(requests.codes.ok)
        self.end_headers()
        return


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
