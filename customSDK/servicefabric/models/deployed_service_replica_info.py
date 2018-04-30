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


class DeployedServiceReplicaInfo(Model):
    """Information about a Service Fabric service replica deployed on a node.

    You probably want to use the sub-classes and not this class directly. Known
    sub-classes are: DeployedStatefulServiceReplicaInfo,
    DeployedStatelessServiceInstanceInfo

    :param service_name: The full name of the service with 'fabric:' URI
     scheme.
    :type service_name: str
    :param service_type_name: Name of the service type as specified in the
     service manifest.
    :type service_type_name: str
    :param service_manifest_name: The name of the service manifest in which
     this service type is defined.
    :type service_manifest_name: str
    :param code_package_name: The name of the code package that hosts this
     replica.
    :type code_package_name: str
    :param partition_id: An internal ID used by Service Fabric to uniquely
     identify a partition. This is a randomly generated GUID when the service
     was created. The partition ID is unique and does not change for the
     lifetime of the service. If the same service was deleted and recreated the
     IDs of its partitions would be different.
    :type partition_id: str
    :param replica_status: The status of a replica of a service. Possible
     values include: 'Invalid', 'InBuild', 'Standby', 'Ready', 'Down',
     'Dropped'
    :type replica_status: str or ~azure.servicefabric.models.ReplicaStatus
    :param address: The last address returned by the replica in Open or
     ChangeRole.
    :type address: str
    :param service_package_activation_id: The ActivationId of a deployed
     service package. If ServicePackageActivationMode specified at the time of
     creating the service
     is 'SharedProcess' (or if it is not specified, in which case it defaults
     to 'SharedProcess'), then value of ServicePackageActivationId
     is always an empty string.
    :type service_package_activation_id: str
    :param host_process_id: Host process ID of the process that is hosting the
     replica. This will be zero if the replica is down. In hyper-v containers
     this host process ID will be from different kernel.
    :type host_process_id: str
    :param service_kind: Constant filled by server.
    :type service_kind: str
    """

    _validation = {
        'service_kind': {'required': True},
    }

    _attribute_map = {
        'service_name': {'key': 'ServiceName', 'type': 'str'},
        'service_type_name': {'key': 'ServiceTypeName', 'type': 'str'},
        'service_manifest_name': {'key': 'ServiceManifestName', 'type': 'str'},
        'code_package_name': {'key': 'CodePackageName', 'type': 'str'},
        'partition_id': {'key': 'PartitionId', 'type': 'str'},
        'replica_status': {'key': 'ReplicaStatus', 'type': 'str'},
        'address': {'key': 'Address', 'type': 'str'},
        'service_package_activation_id': {'key': 'ServicePackageActivationId', 'type': 'str'},
        'host_process_id': {'key': 'HostProcessId', 'type': 'str'},
        'service_kind': {'key': 'ServiceKind', 'type': 'str'},
    }

    _subtype_map = {
        'service_kind': {'Stateful': 'DeployedStatefulServiceReplicaInfo', 'Stateless': 'DeployedStatelessServiceInstanceInfo'}
    }

    def __init__(self, service_name=None, service_type_name=None, service_manifest_name=None, code_package_name=None, partition_id=None, replica_status=None, address=None, service_package_activation_id=None, host_process_id=None):
        self.service_name = service_name
        self.service_type_name = service_type_name
        self.service_manifest_name = service_manifest_name
        self.code_package_name = code_package_name
        self.partition_id = partition_id
        self.replica_status = replica_status
        self.address = address
        self.service_package_activation_id = service_package_activation_id
        self.host_process_id = host_process_id
        self.service_kind = None
