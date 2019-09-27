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


class ResumeApplicationUpgradeDescription(Model):
    """Describes the parameters for resuming an unmonitored manual Service Fabric
    application upgrade.

    All required parameters must be populated in order to send to Azure.

    :param upgrade_domain_name: Required. The name of the upgrade domain in
     which to resume the upgrade.
    :type upgrade_domain_name: str
    """

    _validation = {
        'upgrade_domain_name': {'required': True},
    }

    _attribute_map = {
        'upgrade_domain_name': {'key': 'UpgradeDomainName', 'type': 'str'},
    }

    def __init__(self, **kwargs):
        super(ResumeApplicationUpgradeDescription, self).__init__(**kwargs)
        self.upgrade_domain_name = kwargs.get('upgrade_domain_name', None)
