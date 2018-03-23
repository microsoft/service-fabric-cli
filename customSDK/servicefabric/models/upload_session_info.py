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


class UploadSessionInfo(Model):
    """Information about an image store upload session. A session is associated
    with a relative path in the image store.

    :param store_relative_path: The remote location within image store. This
     path is relative to the image store root.
    :type store_relative_path: str
    :param session_id: A unique ID of the upload session. A session ID can be
     reused only if the session was committed or removed.
    :type session_id: str
    :param modified_date: The date and time when the upload session was last
     modified.
    :type modified_date: datetime
    :param file_size: The size in bytes of the uploading file.
    :type file_size: str
    :param expected_ranges: List of chunk ranges that image store has not
     received yet.
    :type expected_ranges: list[~azure.servicefabric.models.UploadChunkRange]
    """

    _attribute_map = {
        'store_relative_path': {'key': 'StoreRelativePath', 'type': 'str'},
        'session_id': {'key': 'SessionId', 'type': 'str'},
        'modified_date': {'key': 'ModifiedDate', 'type': 'iso-8601'},
        'file_size': {'key': 'FileSize', 'type': 'str'},
        'expected_ranges': {'key': 'ExpectedRanges', 'type': '[UploadChunkRange]'},
    }

    def __init__(self, store_relative_path=None, session_id=None, modified_date=None, file_size=None, expected_ranges=None):
        self.store_relative_path = store_relative_path
        self.session_id = session_id
        self.modified_date = modified_date
        self.file_size = file_size
        self.expected_ranges = expected_ranges
