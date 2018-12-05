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


class HttpConfig(Model):
    """Describes the http configuration for external connectivity for this
    network.

    All required parameters must be populated in order to send to Azure.

    :param name: Required. http gateway config name.
    :type name: str
    :param port: Required. Specifies the port at which the service endpoint
     below needs to be exposed.
    :type port: int
    :param hosts: Required. description for routing.
    :type hosts: list[~azure.servicefabric.models.HttpHostConfig]
    """

    _validation = {
        'name': {'required': True},
        'port': {'required': True},
        'hosts': {'required': True},
    }

    _attribute_map = {
        'name': {'key': 'name', 'type': 'str'},
        'port': {'key': 'port', 'type': 'int'},
        'hosts': {'key': 'hosts', 'type': '[HttpHostConfig]'},
    }

    def __init__(self, **kwargs):
        super(HttpConfig, self).__init__(**kwargs)
        self.name = kwargs.get('name', None)
        self.port = kwargs.get('port', None)
        self.hosts = kwargs.get('hosts', None)
