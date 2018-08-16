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


class ApplicationLoadInfo(Model):
    """Load Information about a Service Fabric application.

    :param id: The identity of the application. This is an encoded
     representation of the application name. This is used in the REST APIs to
     identify the application resource.
     Starting in version 6.0, hierarchical names are delimited with the "\\~"
     character. For example, if the application name is "fabric:/myapp/app1",
     the application identity would be "myapp\\~app1" in 6.0+ and "myapp/app1"
     in previous versions.
    :type id: str
    :param minimum_nodes: The minimum number of nodes for this application.
     It is the number of nodes where Service Fabric will reserve Capacity in
     the cluster which equals to ReservedLoad * MinimumNodes for this
     Application instance.
     For applications that do not have application capacity defined this value
     will be zero.
    :type minimum_nodes: long
    :param maximum_nodes: The maximum number of nodes where this application
     can be instantiated.
     It is the number of nodes this application is allowed to span.
     For applications that do not have application capacity defined this value
     will be zero.
    :type maximum_nodes: long
    :param node_count: The number of nodes on which this application is
     instantiated.
     For applications that do not have application capacity defined this value
     will be zero.
    :type node_count: long
    :param application_load_metric_information: List of application capacity
     metric description.
    :type application_load_metric_information:
     list[~azure.servicefabric.models.ApplicationMetricDescription]
    """

    _attribute_map = {
        'id': {'key': 'Id', 'type': 'str'},
        'minimum_nodes': {'key': 'MinimumNodes', 'type': 'long'},
        'maximum_nodes': {'key': 'MaximumNodes', 'type': 'long'},
        'node_count': {'key': 'NodeCount', 'type': 'long'},
        'application_load_metric_information': {'key': 'ApplicationLoadMetricInformation', 'type': '[ApplicationMetricDescription]'},
    }

    def __init__(self, id=None, minimum_nodes=None, maximum_nodes=None, node_count=None, application_load_metric_information=None):
        super(ApplicationLoadInfo, self).__init__()
        self.id = id
        self.minimum_nodes = minimum_nodes
        self.maximum_nodes = maximum_nodes
        self.node_count = node_count
        self.application_load_metric_information = application_load_metric_information
