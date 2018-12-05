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

from .partition_safety_check_py3 import PartitionSafetyCheck


class WaitForPrimaryPlacementSafetyCheck(PartitionSafetyCheck):
    """Safety check that waits for the primary replica that was moved out of the
    node due to upgrade to be placed back again on that node.

    All required parameters must be populated in order to send to Azure.

    :param kind: Required. Constant filled by server.
    :type kind: str
    :param partition_id: Id of the partition which is undergoing the safety
     check.
    :type partition_id: str
    """

    _validation = {
        'kind': {'required': True},
    }

    _attribute_map = {
        'kind': {'key': 'Kind', 'type': 'str'},
        'partition_id': {'key': 'PartitionId', 'type': 'str'},
    }

    def __init__(self, *, partition_id: str=None, **kwargs) -> None:
        super(WaitForPrimaryPlacementSafetyCheck, self).__init__(partition_id=partition_id, **kwargs)
        self.kind = 'WaitForPrimaryPlacement'
