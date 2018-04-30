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

from .backup_schedule_description import BackupScheduleDescription


class FrequencyBasedBackupScheduleDescription(BackupScheduleDescription):
    """Describes the frequency based backup schedule.

    :param schedule_kind: Constant filled by server.
    :type schedule_kind: str
    :param interval: Defines the interval with which backups are periodically
     taken. It should be specified in ISO8601 format. Timespan in seconds is
     not supported and will be ignored while creating the policy.
    :type interval: timedelta
    """

    _validation = {
        'schedule_kind': {'required': True},
        'interval': {'required': True},
    }

    _attribute_map = {
        'schedule_kind': {'key': 'ScheduleKind', 'type': 'str'},
        'interval': {'key': 'Interval', 'type': 'duration'},
    }

    def __init__(self, interval):
        super(FrequencyBasedBackupScheduleDescription, self).__init__()
        self.interval = interval
        self.schedule_kind = 'FrequencyBased'