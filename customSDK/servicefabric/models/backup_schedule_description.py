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


class BackupScheduleDescription(Model):
    """Describes the backup schedule parameters.

    You probably want to use the sub-classes and not this class directly. Known
    sub-classes are: FrequencyBasedBackupScheduleDescription,
    TimeBasedBackupScheduleDescription

    :param schedule_kind: Constant filled by server.
    :type schedule_kind: str
    """

    _validation = {
        'schedule_kind': {'required': True},
    }

    _attribute_map = {
        'schedule_kind': {'key': 'ScheduleKind', 'type': 'str'},
    }

    _subtype_map = {
        'schedule_kind': {'FrequencyBased': 'FrequencyBasedBackupScheduleDescription', 'TimeBased': 'TimeBasedBackupScheduleDescription'}
    }

    def __init__(self):
        self.schedule_kind = None
