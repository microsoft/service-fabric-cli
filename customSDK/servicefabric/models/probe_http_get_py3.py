# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class ProbeHttpGet(Model):
    """Http probe for the container.

    All required parameters must be populated in order to send to Azure.

    :param port: Required. Port to access for probe.
    :type port: int
    :param path: Path to access on the HTTP request.
    :type path: str
    :param host: Host IP to connect to.
    :type host: str
    :param http_headers: Headers to set in the request.
    :type http_headers: list[~azure.servicefabric.models.ProbeHttpGetHeaders]
    :param scheme: Scheme for the http probe. Can be Http or Https. Possible
     values include: 'http', 'https'
    :type scheme: str or ~azure.servicefabric.models.Scheme
    """

    _validation = {
        'port': {'required': True},
    }

    _attribute_map = {
        'port': {'key': 'port', 'type': 'int'},
        'path': {'key': 'path', 'type': 'str'},
        'host': {'key': 'host', 'type': 'str'},
        'http_headers': {'key': 'httpHeaders', 'type': '[ProbeHttpGetHeaders]'},
        'scheme': {'key': 'scheme', 'type': 'str'},
    }

    def __init__(self, *, port: int, path: str=None, host: str=None, http_headers=None, scheme=None, **kwargs) -> None:
        super(ProbeHttpGet, self).__init__(**kwargs)
        self.port = port
        self.path = path
        self.host = host
        self.http_headers = http_headers
        self.scheme = scheme
