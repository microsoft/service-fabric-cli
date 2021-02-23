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


class ClusterVersion(Model):
    """The cluster version.

    :param version: The Service Fabric cluster runtime version.
    :type version: str
    """

    _attribute_map = {
        'version': {'key': 'Version', 'type': 'str'},
    }

    def __init__(self, *, version: str=None, **kwargs) -> None:
        super(ClusterVersion, self).__init__(**kwargs)
        self.version = version
