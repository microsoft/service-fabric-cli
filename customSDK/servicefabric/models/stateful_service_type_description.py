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

from .service_type_description import ServiceTypeDescription


class StatefulServiceTypeDescription(ServiceTypeDescription):
    """Describes a stateful service type defined in the service manifest of a
    provisioned application type.

    :param is_stateful: Indicates whether the service type is a stateful
     service type or a stateless service type. This property is true if the
     service type is a stateful service type, false otherwise.
    :type is_stateful: bool
    :param service_type_name: Name of the service type as specified in the
     service manifest.
    :type service_type_name: str
    :param placement_constraints: The placement constraint to be used when
     instantiating this service in a Service Fabric cluster.
    :type placement_constraints: str
    :param load_metrics: The service load metrics is given as an array of
     ServiceLoadMetricDescription objects.
    :type load_metrics:
     list[~azure.servicefabric.models.ServiceLoadMetricDescription]
    :param service_placement_policies: List of service placement policy
     descriptions.
    :type service_placement_policies:
     list[~azure.servicefabric.models.ServicePlacementPolicyDescription]
    :param extensions: List of service type extensions.
    :type extensions:
     list[~azure.servicefabric.models.ServiceTypeExtensionDescription]
    :param kind: Constant filled by server.
    :type kind: str
    :param has_persisted_state: A flag indicating whether this is a persistent
     service which stores states on the local disk. If it is then the value of
     this property is true, if not it is false.
    :type has_persisted_state: bool
    """

    _validation = {
        'kind': {'required': True},
    }

    _attribute_map = {
        'is_stateful': {'key': 'IsStateful', 'type': 'bool'},
        'service_type_name': {'key': 'ServiceTypeName', 'type': 'str'},
        'placement_constraints': {'key': 'PlacementConstraints', 'type': 'str'},
        'load_metrics': {'key': 'LoadMetrics', 'type': '[ServiceLoadMetricDescription]'},
        'service_placement_policies': {'key': 'ServicePlacementPolicies', 'type': '[ServicePlacementPolicyDescription]'},
        'extensions': {'key': 'Extensions', 'type': '[ServiceTypeExtensionDescription]'},
        'kind': {'key': 'Kind', 'type': 'str'},
        'has_persisted_state': {'key': 'HasPersistedState', 'type': 'bool'},
    }

    def __init__(self, is_stateful=None, service_type_name=None, placement_constraints=None, load_metrics=None, service_placement_policies=None, extensions=None, has_persisted_state=None):
        super(StatefulServiceTypeDescription, self).__init__(is_stateful=is_stateful, service_type_name=service_type_name, placement_constraints=placement_constraints, load_metrics=load_metrics, service_placement_policies=service_placement_policies, extensions=extensions)
        self.has_persisted_state = has_persisted_state
        self.kind = 'Stateful'
