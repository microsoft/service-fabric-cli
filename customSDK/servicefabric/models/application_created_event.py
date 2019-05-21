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

from .application_event import ApplicationEvent


class ApplicationCreatedEvent(ApplicationEvent):
    """Application Created event.

    :param event_instance_id: The identifier for the FabricEvent instance.
    :type event_instance_id: str
    :param category: The category of event.
    :type category: str
    :param time_stamp: The time event was logged.
    :type time_stamp: datetime
    :param has_correlated_events: Shows there is existing related events
     available.
    :type has_correlated_events: bool
    :param kind: Constant filled by server.
    :type kind: str
    :param application_id: The identity of the application. This is an encoded
     representation of the application name. This is used in the REST APIs to
     identify the application resource.
     Starting in version 6.0, hierarchical names are delimited with the "\\~"
     character. For example, if the application name is "fabric:/myapp/app1",
     the application identity would be "myapp\\~app1" in 6.0+ and "myapp/app1"
     in previous versions.
    :type application_id: str
    :param application_type_name: Application type name.
    :type application_type_name: str
    :param application_type_version: Application type version.
    :type application_type_version: str
    :param application_definition_kind: Application definition kind.
    :type application_definition_kind: str
    """

    _validation = {
        'event_instance_id': {'required': True},
        'time_stamp': {'required': True},
        'kind': {'required': True},
        'application_id': {'required': True},
        'application_type_name': {'required': True},
        'application_type_version': {'required': True},
        'application_definition_kind': {'required': True},
    }

    _attribute_map = {
        'event_instance_id': {'key': 'EventInstanceId', 'type': 'str'},
        'category': {'key': 'Category', 'type': 'str'},
        'time_stamp': {'key': 'TimeStamp', 'type': 'iso-8601'},
        'has_correlated_events': {'key': 'HasCorrelatedEvents', 'type': 'bool'},
        'kind': {'key': 'Kind', 'type': 'str'},
        'application_id': {'key': 'ApplicationId', 'type': 'str'},
        'application_type_name': {'key': 'ApplicationTypeName', 'type': 'str'},
        'application_type_version': {'key': 'ApplicationTypeVersion', 'type': 'str'},
        'application_definition_kind': {'key': 'ApplicationDefinitionKind', 'type': 'str'},
    }

    def __init__(self, event_instance_id, time_stamp, application_id, application_type_name, application_type_version, application_definition_kind, category=None, has_correlated_events=None):
        super(ApplicationCreatedEvent, self).__init__(event_instance_id=event_instance_id, category=category, time_stamp=time_stamp, has_correlated_events=has_correlated_events, application_id=application_id)
        self.application_type_name = application_type_name
        self.application_type_version = application_type_version
        self.application_definition_kind = application_definition_kind
        self.kind = 'ApplicationCreated'
