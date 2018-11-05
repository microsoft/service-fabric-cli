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


class NodeDeactivationInfo(Model):
    """Information about the node deactivation. This information is valid for a
    node that is undergoing deactivation or has already been deactivated.

    :param node_deactivation_intent: The intent or the reason for deactivating
     the node. Following are the possible values for it. Possible values
     include: 'Invalid', 'Pause', 'Restart', 'RemoveData', 'RemoveNode'
    :type node_deactivation_intent: str or
     ~azure.servicefabric.models.NodeDeactivationIntent
    :param node_deactivation_status: The status of node deactivation
     operation. Following are the possible values. Possible values include:
     'None', 'SafetyCheckInProgress', 'SafetyCheckComplete', 'Completed'
    :type node_deactivation_status: str or
     ~azure.servicefabric.models.NodeDeactivationStatus
    :param node_deactivation_task: List of tasks representing the deactivation
     operation on the node.
    :type node_deactivation_task:
     list[~azure.servicefabric.models.NodeDeactivationTask]
    :param pending_safety_checks: List of pending safety checks
    :type pending_safety_checks:
     list[~azure.servicefabric.models.SafetyCheckWrapper]
    """

    _attribute_map = {
        'node_deactivation_intent': {'key': 'NodeDeactivationIntent', 'type': 'str'},
        'node_deactivation_status': {'key': 'NodeDeactivationStatus', 'type': 'str'},
        'node_deactivation_task': {'key': 'NodeDeactivationTask', 'type': '[NodeDeactivationTask]'},
        'pending_safety_checks': {'key': 'PendingSafetyChecks', 'type': '[SafetyCheckWrapper]'},
    }

    def __init__(self, **kwargs):
        super(NodeDeactivationInfo, self).__init__(**kwargs)
        self.node_deactivation_intent = kwargs.get('node_deactivation_intent', None)
        self.node_deactivation_status = kwargs.get('node_deactivation_status', None)
        self.node_deactivation_task = kwargs.get('node_deactivation_task', None)
        self.pending_safety_checks = kwargs.get('pending_safety_checks', None)
