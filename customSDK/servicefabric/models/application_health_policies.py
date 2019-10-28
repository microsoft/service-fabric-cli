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


class ApplicationHealthPolicies(Model):
    """Defines the application health policy map used to evaluate the health of an
    application or one of its children entities.

    :param application_health_policy_map: The wrapper that contains the map
     with application health policies used to evaluate specific applications in
     the cluster.
    :type application_health_policy_map:
     list[~azure.servicefabric.models.ApplicationHealthPolicyMapItem]
    """

    _attribute_map = {
        'application_health_policy_map': {'key': 'ApplicationHealthPolicyMap', 'type': '[ApplicationHealthPolicyMapItem]'},
    }

    def __init__(self, **kwargs):
        super(ApplicationHealthPolicies, self).__init__(**kwargs)
        self.application_health_policy_map = kwargs.get('application_health_policy_map', None)
