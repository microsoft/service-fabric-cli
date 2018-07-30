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

from .backup_storage_description import BackupStorageDescription


class FileShareBackupStorageDescription(BackupStorageDescription):
    """Describes the parameters for file share storage used for storing or
    enumerating backups.

    :param friendly_name: Friendly name for this backup storage.
    :type friendly_name: str
    :param storage_kind: Constant filled by server.
    :type storage_kind: str
    :param path: UNC path of the file share where to store or enumerate
     backups from.
    :type path: str
    :param primary_user_name: Primary user name to access the file share.
    :type primary_user_name: str
    :param primary_password: Primary password to access the share location.
    :type primary_password: str
    :param secondary_user_name: Secondary user name to access the file share.
    :type secondary_user_name: str
    :param secondary_password: Secondary password to access the share location
    :type secondary_password: str
    """

    _validation = {
        'storage_kind': {'required': True},
        'path': {'required': True},
    }

    _attribute_map = {
        'friendly_name': {'key': 'FriendlyName', 'type': 'str'},
        'storage_kind': {'key': 'StorageKind', 'type': 'str'},
        'path': {'key': 'Path', 'type': 'str'},
        'primary_user_name': {'key': 'PrimaryUserName', 'type': 'str'},
        'primary_password': {'key': 'PrimaryPassword', 'type': 'str'},
        'secondary_user_name': {'key': 'SecondaryUserName', 'type': 'str'},
        'secondary_password': {'key': 'SecondaryPassword', 'type': 'str'},
    }

    def __init__(self, path, friendly_name=None, primary_user_name=None, primary_password=None, secondary_user_name=None, secondary_password=None):
        super(FileShareBackupStorageDescription, self).__init__(friendly_name=friendly_name)
        self.path = path
        self.primary_user_name = primary_user_name
        self.primary_password = primary_password
        self.secondary_user_name = secondary_user_name
        self.secondary_password = secondary_password
        self.storage_kind = 'FileShare'
