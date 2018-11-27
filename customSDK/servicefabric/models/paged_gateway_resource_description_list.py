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


class PagedGatewayResourceDescriptionList(Model):
    """The list of gateway resources. The list is paged when all of the results
    cannot fit in a single message. The next set of results can be obtained by
    executing the same query with the continuation token provided in this list.

    :param continuation_token: The continuation token parameter is used to
     obtain next set of results. The continuation token is included in the
     response of the API when the results from the system do not fit in a
     single response. When this value is passed to the next API call, the API
     returns next set of results. If there are no further results, then the
     continuation token is not included in the response.
    :type continuation_token: str
    :param items: One page of the list.
    :type items: list[~azure.servicefabric.models.GatewayResourceDescription]
    """

    _attribute_map = {
        'continuation_token': {'key': 'ContinuationToken', 'type': 'str'},
        'items': {'key': 'Items', 'type': '[GatewayResourceDescription]'},
    }

    def __init__(self, continuation_token=None, items=None):
        super(PagedGatewayResourceDescriptionList, self).__init__()
        self.continuation_token = continuation_token
        self.items = items
