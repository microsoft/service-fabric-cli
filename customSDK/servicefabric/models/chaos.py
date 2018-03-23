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


class Chaos(Model):
    """Contains a description of Chaos.
    .

    :param chaos_parameters: If Chaos is running, these are the parameters
     Chaos is running with.
    :type chaos_parameters: ~azure.servicefabric.models.ChaosParameters
    :param status: Current status of the Chaos run.
     . Possible values include: 'Invalid', 'Running', 'Stopped'
    :type status: str or ~azure.servicefabric.models.ChaosStatus
    :param schedule_status: Current status of the schedule.
     . Possible values include: 'Invalid', 'Stopped', 'Active', 'Expired',
     'Pending'
    :type schedule_status: str or
     ~azure.servicefabric.models.ChaosScheduleStatus
    """

    _attribute_map = {
        'chaos_parameters': {'key': 'ChaosParameters', 'type': 'ChaosParameters'},
        'status': {'key': 'Status', 'type': 'str'},
        'schedule_status': {'key': 'ScheduleStatus', 'type': 'str'},
    }

    def __init__(self, chaos_parameters=None, status=None, schedule_status=None):
        self.chaos_parameters = chaos_parameters
        self.status = status
        self.schedule_status = schedule_status
