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


class LoadedPartitionInformationQueryDescription(Model):
    """Represents data structure that contains query information.

    :param metric_name: Name of the metric for which this information is
     provided.
    :type metric_name: str
    :param service_name: Name of the service this partition belongs to.
    :type service_name: str
    :param ordering: Ordering of partitions' load. Possible values include:
     'Desc', 'Asc'. Default value: "Desc" .
    :type ordering: str or ~azure.servicefabric.models.Ordering
    :param max_results: The maximum number of results to be returned as part
     of the paged queries. This parameter defines the upper bound on the number
     of results returned. The results returned can be less than the specified
     maximum results if they do not fit in the message as per the max message
     size restrictions defined in the configuration. If this parameter is zero
     or not specified, the paged query includes as many results as possible
     that fit in the return message.
    :type max_results: long
    :param continuation_token: The continuation token parameter is used to
     obtain next set of results. The continuation token is included in the
     response of the API when the results from the system do not fit in a
     single response. When this value is passed to the next API call, the API
     returns next set of results. If there are no further results, then the
     continuation token is not included in the response.
    :type continuation_token: str
    """

    _attribute_map = {
        'metric_name': {'key': 'MetricName', 'type': 'str'},
        'service_name': {'key': 'ServiceName', 'type': 'str'},
        'ordering': {'key': 'Ordering', 'type': 'str'},
        'max_results': {'key': 'MaxResults', 'type': 'long'},
        'continuation_token': {'key': 'ContinuationToken', 'type': 'str'},
    }

    def __init__(self, **kwargs):
        super(LoadedPartitionInformationQueryDescription, self).__init__(**kwargs)
        self.metric_name = kwargs.get('metric_name', None)
        self.service_name = kwargs.get('service_name', None)
        self.ordering = kwargs.get('ordering', "Desc")
        self.max_results = kwargs.get('max_results', None)
        self.continuation_token = kwargs.get('continuation_token', None)
