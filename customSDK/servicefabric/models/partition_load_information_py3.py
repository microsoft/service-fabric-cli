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


class PartitionLoadInformation(Model):
    """Represents load information for a partition, which contains the primary and
    secondary reported load metrics.
    In case there is no load reported, PartitionLoadInformation will contain
    the default load for the service of the partition.
    For default loads, LoadMetricReport's LastReportedUtc is set to 0.

    :param partition_id: Id of the partition.
    :type partition_id: str
    :param primary_load_metric_reports: Array of load reports from the primary
     replica for this partition.
    :type primary_load_metric_reports:
     list[~azure.servicefabric.models.LoadMetricReport]
    :param secondary_load_metric_reports: Array of aggregated load reports
     from all secondary replicas for this partition.
     Array only contains the latest reported load for each metric.
    :type secondary_load_metric_reports:
     list[~azure.servicefabric.models.LoadMetricReport]
    """

    _attribute_map = {
        'partition_id': {'key': 'PartitionId', 'type': 'str'},
        'primary_load_metric_reports': {'key': 'PrimaryLoadMetricReports', 'type': '[LoadMetricReport]'},
        'secondary_load_metric_reports': {'key': 'SecondaryLoadMetricReports', 'type': '[LoadMetricReport]'},
    }

    def __init__(self, *, partition_id: str=None, primary_load_metric_reports=None, secondary_load_metric_reports=None, **kwargs) -> None:
        super(PartitionLoadInformation, self).__init__(**kwargs)
        self.partition_id = partition_id
        self.primary_load_metric_reports = primary_load_metric_reports
        self.secondary_load_metric_reports = secondary_load_metric_reports
