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

from .provision_application_type_description_base import ProvisionApplicationTypeDescriptionBase


class ExternalStoreProvisionApplicationTypeDescription(ProvisionApplicationTypeDescriptionBase):
    """Describes the operation to register or provision an application type using
    an application package from an external store instead of a package uploaded
    to the Service Fabric image store.

    :param async: Indicates whether or not provisioning should occur
     asynchronously. When set to true, the provision operation returns when the
     request is accepted by the system, and the provision operation continues
     without any timeout limit. The default value is false. For large
     application packages, we recommend setting the value to true.
    :type async: bool
    :param kind: Constant filled by server.
    :type kind: str
    :param application_package_download_uri: The path to the '.sfpkg'
     application package from where the application package can be downloaded
     using HTTP or HTTPS protocols. The application package can be stored in an
     external store that provides GET operation to download the file. Supported
     protocols are HTTP and HTTPS, and the path must allow READ access.
    :type application_package_download_uri: str
    :param application_type_name: The application type name represents the
     name of the application type found in the application manifest.
    :type application_type_name: str
    :param application_type_version: The application type version represents
     the version of the application type found in the application manifest.
    :type application_type_version: str
    """

    _validation = {
        'async': {'required': True},
        'kind': {'required': True},
        'application_package_download_uri': {'required': True},
        'application_type_name': {'required': True},
        'application_type_version': {'required': True},
    }

    _attribute_map = {
        'async': {'key': 'Async', 'type': 'bool'},
        'kind': {'key': 'Kind', 'type': 'str'},
        'application_package_download_uri': {'key': 'ApplicationPackageDownloadUri', 'type': 'str'},
        'application_type_name': {'key': 'ApplicationTypeName', 'type': 'str'},
        'application_type_version': {'key': 'ApplicationTypeVersion', 'type': 'str'},
    }

    def __init__(self, async, application_package_download_uri, application_type_name, application_type_version):
        super(ExternalStoreProvisionApplicationTypeDescription, self).__init__(async=async)
        self.application_package_download_uri = application_package_download_uri
        self.application_type_name = application_type_name
        self.application_type_version = application_type_version
        self.kind = 'ExternalStore'
