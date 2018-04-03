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


class RemoteReplicatorAcknowledgementDetail(Model):
    """Provides various statistics of the acknowledgements that are being received
    from the remote replicator.

    :param average_receive_duration: Represents the average duration it takes
     for the remote replicator to receive an operation.
    :type average_receive_duration: str
    :param average_apply_duration: Represents the average duration it takes
     for the remote replicator to apply an operation. This usually entails
     writing the operation to disk.
    :type average_apply_duration: str
    :param not_received_count: Represents the number of operations not yet
     received by a remote replicator.
    :type not_received_count: str
    :param received_and_not_applied_count: Represents the number of operations
     received and not yet applied by a remote replicator.
    :type received_and_not_applied_count: str
    """

    _attribute_map = {
        'average_receive_duration': {'key': 'AverageReceiveDuration', 'type': 'str'},
        'average_apply_duration': {'key': 'AverageApplyDuration', 'type': 'str'},
        'not_received_count': {'key': 'NotReceivedCount', 'type': 'str'},
        'received_and_not_applied_count': {'key': 'ReceivedAndNotAppliedCount', 'type': 'str'},
    }

    def __init__(self, average_receive_duration=None, average_apply_duration=None, not_received_count=None, received_and_not_applied_count=None):
        self.average_receive_duration = average_receive_duration
        self.average_apply_duration = average_apply_duration
        self.not_received_count = not_received_count
        self.received_and_not_applied_count = received_and_not_applied_count
