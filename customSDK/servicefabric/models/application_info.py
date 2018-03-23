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


class ApplicationInfo(Model):
    """Information about a Service Fabric application.

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
    :param type_version: The version of the application type as defined in the
     application manifest.
    :type type_version: str
    :param status: The status of the application.
     . Possible values include: 'Invalid', 'Ready', 'Upgrading', 'Creating',
     'Deleting', 'Failed'
    :type status: str or ~azure.servicefabric.models.ApplicationStatus
    :param parameters: List of application parameters with overridden values
     from their default values specified in the application manifest.
    :type parameters: list[~azure.servicefabric.models.ApplicationParameter]
    :param health_state: The health state of a Service Fabric entity such as
     Cluster, Node, Application, Service, Partition, Replica etc. Possible
     values include: 'Invalid', 'Ok', 'Warning', 'Error', 'Unknown'
    :type health_state: str or ~azure.servicefabric.models.HealthState
    :param application_definition_kind: The mechanism used to define a Service
     Fabric application.
     . Possible values include: 'Invalid',
     'ServiceFabricApplicationDescription', 'Compose'
    :type application_definition_kind: str or
     ~azure.servicefabric.models.ApplicationDefinitionKind
    """

    _attribute_map = {
        'id': {'key': 'Id', 'type': 'str'},
        'name': {'key': 'Name', 'type': 'str'},
        'type_name': {'key': 'TypeName', 'type': 'str'},
        'type_version': {'key': 'TypeVersion', 'type': 'str'},
        'status': {'key': 'Status', 'type': 'str'},
        'parameters': {'key': 'Parameters', 'type': '[ApplicationParameter]'},
        'health_state': {'key': 'HealthState', 'type': 'str'},
        'application_definition_kind': {'key': 'ApplicationDefinitionKind', 'type': 'str'},
    }

    def __init__(self, id=None, name=None, type_name=None, type_version=None, status=None, parameters=None, health_state=None, application_definition_kind=None):
        self.id = id
        self.name = name
        self.type_name = type_name
        self.type_version = type_version
        self.status = status
        self.parameters = parameters
        self.health_state = health_state
        self.application_definition_kind = application_definition_kind
