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


class DeployedApplicationInfo(Model):
    """Information about application deployed on the node.

    :param id: The identity of the application. This is an encoded
     representation of the application name. This is used in the REST APIs to
     identify the application resource.
     Starting in version 6.0, hierarchical names are delimited with the "\\~"
     character. For example, if the application name is "fabric:/myapp/app1",
     the application identity would be "myapp\\~app1" in 6.0+ and "myapp/app1"
     in previous versions.
    :type id: str
    :param name: The name of the application, including the 'fabric:' URI
     scheme.
    :type name: str
    :param type_name: The application type name as defined in the application
     manifest.
    :type type_name: str
    :param status: The status of the application deployed on the node.
     Following are the possible values. Possible values include: 'Invalid',
     'Downloading', 'Activating', 'Active', 'Upgrading', 'Deactivating'
    :type status: str or ~azure.servicefabric.models.DeployedApplicationStatus
    :param work_directory: The work directory of the application on the node.
     The work directory can be used to store application data.
    :type work_directory: str
    :param log_directory: The log directory of the application on the node.
     The log directory can be used to store application logs.
    :type log_directory: str
    :param temp_directory: The temp directory of the application on the node.
     The code packages belonging to the application are forked with this
     directory set as their temporary directory.
    :type temp_directory: str
    :param health_state: The health state of a Service Fabric entity such as
     Cluster, Node, Application, Service, Partition, Replica etc. Possible
     values include: 'Invalid', 'Ok', 'Warning', 'Error', 'Unknown'
    :type health_state: str or ~azure.servicefabric.models.HealthState
    """

    _attribute_map = {
        'id': {'key': 'Id', 'type': 'str'},
        'name': {'key': 'Name', 'type': 'str'},
        'type_name': {'key': 'TypeName', 'type': 'str'},
        'status': {'key': 'Status', 'type': 'str'},
        'work_directory': {'key': 'WorkDirectory', 'type': 'str'},
        'log_directory': {'key': 'LogDirectory', 'type': 'str'},
        'temp_directory': {'key': 'TempDirectory', 'type': 'str'},
        'health_state': {'key': 'HealthState', 'type': 'str'},
    }

    def __init__(self, *, id: str=None, name: str=None, type_name: str=None, status=None, work_directory: str=None, log_directory: str=None, temp_directory: str=None, health_state=None, **kwargs) -> None:
        super(DeployedApplicationInfo, self).__init__(**kwargs)
        self.id = id
        self.name = name
        self.type_name = type_name
        self.status = status
        self.work_directory = work_directory
        self.log_directory = log_directory
        self.temp_directory = temp_directory
        self.health_state = health_state
