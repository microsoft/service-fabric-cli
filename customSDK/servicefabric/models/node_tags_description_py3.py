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


class NodeTagsDescription(Model):
    """Describes the tags required for placement or running of the service.

    All required parameters must be populated in order to send to Azure.

    :param count: Required. The number of tags.
    :type count: int
    :param tags: Required. Array of size specified by the ‘Count’ parameter,
     for the placement tags of the service.
    :type tags: list[str]
    """

    _validation = {
        'count': {'required': True},
        'tags': {'required': True},
    }

    _attribute_map = {
        'count': {'key': 'Count', 'type': 'int'},
        'tags': {'key': 'Tags', 'type': '[str]'},
    }

    def __init__(self, *, count: int, tags, **kwargs) -> None:
        super(NodeTagsDescription, self).__init__(**kwargs)
        self.count = count
        self.tags = tags
