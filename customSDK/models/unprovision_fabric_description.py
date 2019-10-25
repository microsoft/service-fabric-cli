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


class UnprovisionFabricDescription(Model):
    """Describes the parameters for unprovisioning a cluster.

    :param code_version: The cluster code package version.
    :type code_version: str
    :param config_version: The cluster manifest version.
    :type config_version: str
    """

    _attribute_map = {
        'code_version': {'key': 'CodeVersion', 'type': 'str'},
        'config_version': {'key': 'ConfigVersion', 'type': 'str'},
    }

    def __init__(self, **kwargs):
        super(UnprovisionFabricDescription, self).__init__(**kwargs)
        self.code_version = kwargs.get('code_version', None)
        self.config_version = kwargs.get('config_version', None)
