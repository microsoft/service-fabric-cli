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


class UsageInfo(Model):
    """Information about how much space and how many files in the file system the
    ImageStore is using in this category.

    :param used_space: the size of all files in this category
    :type used_space: str
    :param file_count: the number of all files in this category
    :type file_count: str
    """

    _attribute_map = {
        'used_space': {'key': 'UsedSpace', 'type': 'str'},
        'file_count': {'key': 'FileCount', 'type': 'str'},
    }

    def __init__(self, *, used_space: str=None, file_count: str=None, **kwargs) -> None:
        super(UsageInfo, self).__init__(**kwargs)
        self.used_space = used_space
        self.file_count = file_count
