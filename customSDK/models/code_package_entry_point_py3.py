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


class CodePackageEntryPoint(Model):
    """Information about setup or main entry point of a code package deployed on a
    Service Fabric node.

    :param entry_point_location: The location of entry point executable on the
     node.
    :type entry_point_location: str
    :param process_id: The process ID of the entry point.
    :type process_id: str
    :param run_as_user_name: The user name under which entry point executable
     is run on the node.
    :type run_as_user_name: str
    :param code_package_entry_point_statistics: Statistics about setup or main
     entry point  of a code package deployed on a Service Fabric node.
    :type code_package_entry_point_statistics:
     ~azure.servicefabric.models.CodePackageEntryPointStatistics
    :param status: Specifies the status of the code package entry point
     deployed on a Service Fabric node. Possible values include: 'Invalid',
     'Pending', 'Starting', 'Started', 'Stopping', 'Stopped'
    :type status: str or ~azure.servicefabric.models.EntryPointStatus
    :param next_activation_time: The time (in UTC) when the entry point
     executable will be run next.
    :type next_activation_time: datetime
    :param instance_id: The instance ID for current running entry point. For a
     code package setup entry point (if specified) runs first and after it
     finishes main entry point is started. Each time entry point executable is
     run, its instance id will change.
    :type instance_id: str
    """

    _attribute_map = {
        'entry_point_location': {'key': 'EntryPointLocation', 'type': 'str'},
        'process_id': {'key': 'ProcessId', 'type': 'str'},
        'run_as_user_name': {'key': 'RunAsUserName', 'type': 'str'},
        'code_package_entry_point_statistics': {'key': 'CodePackageEntryPointStatistics', 'type': 'CodePackageEntryPointStatistics'},
        'status': {'key': 'Status', 'type': 'str'},
        'next_activation_time': {'key': 'NextActivationTime', 'type': 'iso-8601'},
        'instance_id': {'key': 'InstanceId', 'type': 'str'},
    }

    def __init__(self, *, entry_point_location: str=None, process_id: str=None, run_as_user_name: str=None, code_package_entry_point_statistics=None, status=None, next_activation_time=None, instance_id: str=None, **kwargs) -> None:
        super(CodePackageEntryPoint, self).__init__(**kwargs)
        self.entry_point_location = entry_point_location
        self.process_id = process_id
        self.run_as_user_name = run_as_user_name
        self.code_package_entry_point_statistics = code_package_entry_point_statistics
        self.status = status
        self.next_activation_time = next_activation_time
        self.instance_id = instance_id
