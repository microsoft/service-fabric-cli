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


class CodePackageEntryPointStatistics(Model):
    """Statistics about setup or main entry point  of a code package deployed on a
    Service Fabric node.

    :param last_exit_code: The last exit code of the entry point.
    :type last_exit_code: str
    :param last_activation_time: The last time (in UTC) when Service Fabric
     attempted to run the entry point.
    :type last_activation_time: datetime
    :param last_exit_time: The last time (in UTC) when the entry point
     finished running.
    :type last_exit_time: datetime
    :param last_successful_activation_time: The last time (in UTC) when the
     entry point ran successfully.
    :type last_successful_activation_time: datetime
    :param last_successful_exit_time: The last time (in UTC) when the entry
     point finished running gracefully.
    :type last_successful_exit_time: datetime
    :param activation_count: Number of times the entry point has run.
    :type activation_count: str
    :param activation_failure_count: Number of times the entry point failed to
     run.
    :type activation_failure_count: str
    :param continuous_activation_failure_count: Number of times the entry
     point continuously failed to run.
    :type continuous_activation_failure_count: str
    :param exit_count: Number of times the entry point finished running.
    :type exit_count: str
    :param exit_failure_count: Number of times the entry point failed to exit
     gracefully.
    :type exit_failure_count: str
    :param continuous_exit_failure_count: Number of times the entry point
     continuously failed to exit gracefully.
    :type continuous_exit_failure_count: str
    """

    _attribute_map = {
        'last_exit_code': {'key': 'LastExitCode', 'type': 'str'},
        'last_activation_time': {'key': 'LastActivationTime', 'type': 'iso-8601'},
        'last_exit_time': {'key': 'LastExitTime', 'type': 'iso-8601'},
        'last_successful_activation_time': {'key': 'LastSuccessfulActivationTime', 'type': 'iso-8601'},
        'last_successful_exit_time': {'key': 'LastSuccessfulExitTime', 'type': 'iso-8601'},
        'activation_count': {'key': 'ActivationCount', 'type': 'str'},
        'activation_failure_count': {'key': 'ActivationFailureCount', 'type': 'str'},
        'continuous_activation_failure_count': {'key': 'ContinuousActivationFailureCount', 'type': 'str'},
        'exit_count': {'key': 'ExitCount', 'type': 'str'},
        'exit_failure_count': {'key': 'ExitFailureCount', 'type': 'str'},
        'continuous_exit_failure_count': {'key': 'ContinuousExitFailureCount', 'type': 'str'},
    }

    def __init__(self, last_exit_code=None, last_activation_time=None, last_exit_time=None, last_successful_activation_time=None, last_successful_exit_time=None, activation_count=None, activation_failure_count=None, continuous_activation_failure_count=None, exit_count=None, exit_failure_count=None, continuous_exit_failure_count=None):
        super(CodePackageEntryPointStatistics, self).__init__()
        self.last_exit_code = last_exit_code
        self.last_activation_time = last_activation_time
        self.last_exit_time = last_exit_time
        self.last_successful_activation_time = last_successful_activation_time
        self.last_successful_exit_time = last_successful_exit_time
        self.activation_count = activation_count
        self.activation_failure_count = activation_failure_count
        self.continuous_activation_failure_count = continuous_activation_failure_count
        self.exit_count = exit_count
        self.exit_failure_count = exit_failure_count
        self.continuous_exit_failure_count = continuous_exit_failure_count
