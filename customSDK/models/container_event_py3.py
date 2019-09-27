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


class ContainerEvent(Model):
    """A container event.

    :param name: The name of the container event.
    :type name: str
    :param count: The count of the event.
    :type count: int
    :param first_timestamp: Date/time of the first event.
    :type first_timestamp: str
    :param last_timestamp: Date/time of the last event.
    :type last_timestamp: str
    :param message: The event message
    :type message: str
    :param type: The event type.
    :type type: str
    """

    _attribute_map = {
        'name': {'key': 'name', 'type': 'str'},
        'count': {'key': 'count', 'type': 'int'},
        'first_timestamp': {'key': 'firstTimestamp', 'type': 'str'},
        'last_timestamp': {'key': 'lastTimestamp', 'type': 'str'},
        'message': {'key': 'message', 'type': 'str'},
        'type': {'key': 'type', 'type': 'str'},
    }

    def __init__(self, *, name: str=None, count: int=None, first_timestamp: str=None, last_timestamp: str=None, message: str=None, type: str=None, **kwargs) -> None:
        super(ContainerEvent, self).__init__(**kwargs)
        self.name = name
        self.count = count
        self.first_timestamp = first_timestamp
        self.last_timestamp = last_timestamp
        self.message = message
        self.type = type
