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


class ChaosEventsSegment(Model):
    """Contains the list of Chaos events and the continuation token to get the
    next segment.

    :param continuation_token: The continuation token parameter is used to
     obtain next set of results. The continuation token is included in the
     response of the API when the results from the system do not fit in a
     single response. When this value is passed to the next API call, the API
     returns next set of results. If there are no further results then the
     continuation token is not included in the response.
    :type continuation_token: str
    :param history: List of Chaos events that meet the user-supplied criteria.
    :type history: list[~azure.servicefabric.models.ChaosEventWrapper]
    """

    _attribute_map = {
        'continuation_token': {'key': 'ContinuationToken', 'type': 'str'},
        'history': {'key': 'History', 'type': '[ChaosEventWrapper]'},
    }

    def __init__(self, *, continuation_token: str=None, history=None, **kwargs) -> None:
        super(ChaosEventsSegment, self).__init__(**kwargs)
        self.continuation_token = continuation_token
        self.history = history
