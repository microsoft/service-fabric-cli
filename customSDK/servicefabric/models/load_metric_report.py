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


class LoadMetricReport(Model):
    """Represents the load metric report which contains the time metric was
    reported, its name and value.

    :param last_reported_utc: Gets the UTC time when the load was reported.
    :type last_reported_utc: datetime
    :param name: The name of the load metric.
    :type name: str
    :param value: The value of the load metric.
    :type value: str
    """

    _attribute_map = {
        'last_reported_utc': {'key': 'LastReportedUtc', 'type': 'iso-8601'},
        'name': {'key': 'Name', 'type': 'str'},
        'value': {'key': 'Value', 'type': 'str'},
    }

    def __init__(self, **kwargs):
        super(LoadMetricReport, self).__init__(**kwargs)
        self.last_reported_utc = kwargs.get('last_reported_utc', None)
        self.name = kwargs.get('name', None)
        self.value = kwargs.get('value', None)
