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

from .secret_resource_properties_base_py3 import SecretResourcePropertiesBase


class SecretResourceProperties(SecretResourcePropertiesBase):
    """Describes the properties of a secret resource.

    You probably want to use the sub-classes and not this class directly. Known
    sub-classes are: InlinedValueSecretResourceProperties

    Variables are only populated by the server, and will be ignored when
    sending a request.

    All required parameters must be populated in order to send to Azure.

    :param kind: Required. Constant filled by server.
    :type kind: str
    :param description: User readable description of the secret.
    :type description: str
    :ivar status: Status of the resource. Possible values include: 'Unknown',
     'Ready', 'Upgrading', 'Creating', 'Deleting', 'Failed'
    :vartype status: str or ~azure.servicefabric.models.ResourceStatus
    :ivar status_details: Gives additional information about the current
     status of the secret.
    :vartype status_details: str
    :param content_type: The type of the content stored in the secret value.
     The value of this property is opaque to Service Fabric. Once set, the
     value of this property cannot be changed.
    :type content_type: str
    """

    _validation = {
        'kind': {'required': True},
        'status': {'readonly': True},
        'status_details': {'readonly': True},
    }

    _attribute_map = {
        'kind': {'key': 'kind', 'type': 'str'},
        'description': {'key': 'description', 'type': 'str'},
        'status': {'key': 'status', 'type': 'str'},
        'status_details': {'key': 'statusDetails', 'type': 'str'},
        'content_type': {'key': 'contentType', 'type': 'str'},
    }

    _subtype_map = {
        'kind': {'inlinedValue': 'InlinedValueSecretResourceProperties'}
    }

    def __init__(self, *, description: str=None, content_type: str=None, **kwargs) -> None:
        super(SecretResourceProperties, self).__init__(**kwargs)
        self.description = description
        self.status = None
        self.status_details = None
        self.content_type = content_type
        self.kind = 'SecretResourceProperties'
