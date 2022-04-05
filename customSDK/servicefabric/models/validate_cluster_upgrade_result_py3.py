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


class ValidateClusterUpgradeResult(Model):
    """Specifies result of validating a cluster upgrade.

    :param service_host_upgrade_impact: The expected impact of the upgrade.
     Possible values include: 'Invalid', 'None', 'ServiceHostRestart',
     'UnexpectedServiceHostRestart'
    :type service_host_upgrade_impact: str or
     ~azure.servicefabric.models.ServiceHostUpgradeImpact
    :param validation_details: A string containing additional details for the
     Fabric upgrade validation result.
    :type validation_details: str
    """

    _attribute_map = {
        'service_host_upgrade_impact': {'key': 'ServiceHostUpgradeImpact', 'type': 'str'},
        'validation_details': {'key': 'ValidationDetails', 'type': 'str'},
    }

    def __init__(self, *, service_host_upgrade_impact=None, validation_details: str=None, **kwargs) -> None:
        super(ValidateClusterUpgradeResult, self).__init__(**kwargs)
        self.service_host_upgrade_impact = service_host_upgrade_impact
        self.validation_details = validation_details
