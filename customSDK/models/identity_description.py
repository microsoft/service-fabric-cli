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


class IdentityDescription(Model):
    """Information describing the identities associated with this application.

    All required parameters must be populated in order to send to Azure.

    :param token_service_endpoint: the endpoint for the token service managing
     this identity
    :type token_service_endpoint: str
    :param type: Required. the types of identities associated with this
     resource; currently restricted to 'SystemAssigned and UserAssigned'
    :type type: str
    :param tenant_id: the identifier of the tenant containing the
     application's identity.
    :type tenant_id: str
    :param principal_id: the object identifier of the Service Principal of the
     identity associated with this resource.
    :type principal_id: str
    :param user_assigned_identities: represents user assigned identities map.
    :type user_assigned_identities: dict[str,
     ~azure.servicefabric.models.IdentityItemDescription]
    """

    _validation = {
        'type': {'required': True},
    }

    _attribute_map = {
        'token_service_endpoint': {'key': 'tokenServiceEndpoint', 'type': 'str'},
        'type': {'key': 'type', 'type': 'str'},
        'tenant_id': {'key': 'tenantId', 'type': 'str'},
        'principal_id': {'key': 'principalId', 'type': 'str'},
        'user_assigned_identities': {'key': 'userAssignedIdentities', 'type': '{IdentityItemDescription}'},
    }

    def __init__(self, **kwargs):
        super(IdentityDescription, self).__init__(**kwargs)
        self.token_service_endpoint = kwargs.get('token_service_endpoint', None)
        self.type = kwargs.get('type', None)
        self.tenant_id = kwargs.get('tenant_id', None)
        self.principal_id = kwargs.get('principal_id', None)
        self.user_assigned_identities = kwargs.get('user_assigned_identities', None)
