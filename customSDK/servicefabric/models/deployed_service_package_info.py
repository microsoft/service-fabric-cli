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


class DeployedServicePackageInfo(Model):
    """Information about service package deployed on a Service Fabric node.

    :param name: The name of the service package as specified in the service
     manifest.
    :type name: str
    :param version: The version of the service package specified in service
     manifest.
    :type version: str
    :param status: Specifies the status of a deployed application or service
     package on a Service Fabric node. Possible values include: 'Invalid',
     'Downloading', 'Activating', 'Active', 'Upgrading', 'Deactivating'
    :type status: str or ~azure.servicefabric.models.DeploymentStatus
    :param service_package_activation_id: The ActivationId of a deployed
     service package. If ServicePackageActivationMode specified at the time of
     creating the service
     is 'SharedProcess' (or if it is not specified, in which case it defaults
     to 'SharedProcess'), then value of ServicePackageActivationId
     is always an empty string.
    :type service_package_activation_id: str
    """

    _attribute_map = {
        'name': {'key': 'Name', 'type': 'str'},
        'version': {'key': 'Version', 'type': 'str'},
        'status': {'key': 'Status', 'type': 'str'},
        'service_package_activation_id': {'key': 'ServicePackageActivationId', 'type': 'str'},
    }

    def __init__(self, name=None, version=None, status=None, service_package_activation_id=None):
        super(DeployedServicePackageInfo, self).__init__()
        self.name = name
        self.version = version
        self.status = status
        self.service_package_activation_id = service_package_activation_id
