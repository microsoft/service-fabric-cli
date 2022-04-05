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


class CurrentUpgradeUnitsProgressInfo(Model):
    """Information about the current in-progress upgrade units.

    :param domain_name: The name of the upgrade domain. Not applicable to
     node-by-node upgrades.
    :type domain_name: str
    :param node_upgrade_progress_list: List of upgrading nodes and their
     statuses
    :type node_upgrade_progress_list:
     list[~azure.servicefabric.models.NodeUpgradeProgressInfo]
    """

    _attribute_map = {
        'domain_name': {'key': 'DomainName', 'type': 'str'},
        'node_upgrade_progress_list': {'key': 'NodeUpgradeProgressList', 'type': '[NodeUpgradeProgressInfo]'},
    }

    def __init__(self, *, domain_name: str=None, node_upgrade_progress_list=None, **kwargs) -> None:
        super(CurrentUpgradeUnitsProgressInfo, self).__init__(**kwargs)
        self.domain_name = domain_name
        self.node_upgrade_progress_list = node_upgrade_progress_list
