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

from .service_placement_policy_description import ServicePlacementPolicyDescription


class ServicePlacementNonPartiallyPlaceServicePolicyDescription(ServicePlacementPolicyDescription):
    """Describes the policy to be used for placement of a Service Fabric service
    where all replicas must be able to be placed in order for any replicas to
    be created.

    :param type: Constant filled by server.
    :type type: str
    """

    _validation = {
        'type': {'required': True},
    }

    def __init__(self):
        super(ServicePlacementNonPartiallyPlaceServicePolicyDescription, self).__init__()
        self.type = 'NonPartiallyPlaceService'
