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


class RollingUpgradeUpdateDescription(Model):
    """Describes the parameters for updating a rolling upgrade of application or
    cluster.

    All required parameters must be populated in order to send to Azure.

    :param rolling_upgrade_mode: Required. The mode used to monitor health
     during a rolling upgrade. The values are UnmonitoredAuto,
     UnmonitoredManual, and Monitored. Possible values include: 'Invalid',
     'UnmonitoredAuto', 'UnmonitoredManual', 'Monitored'. Default value:
     "UnmonitoredAuto" .
    :type rolling_upgrade_mode: str or ~azure.servicefabric.models.UpgradeMode
    :param force_restart: If true, then processes are forcefully restarted
     during upgrade even when the code version has not changed (the upgrade
     only changes configuration or data).
    :type force_restart: bool
    :param replica_set_check_timeout_in_milliseconds: The maximum amount of
     time to block processing of an upgrade domain and prevent loss of
     availability when there are unexpected issues. When this timeout expires,
     processing of the upgrade domain will proceed regardless of availability
     loss issues. The timeout is reset at the start of each upgrade domain.
     Valid values are between 0 and 42949672925 inclusive. (unsigned 32-bit
     integer).
    :type replica_set_check_timeout_in_milliseconds: long
    :param failure_action: The compensating action to perform when a Monitored
     upgrade encounters monitoring policy or health policy violations.
     Invalid indicates the failure action is invalid. Rollback specifies that
     the upgrade will start rolling back automatically.
     Manual indicates that the upgrade will switch to UnmonitoredManual upgrade
     mode. Possible values include: 'Invalid', 'Rollback', 'Manual'
    :type failure_action: str or ~azure.servicefabric.models.FailureAction
    :param health_check_wait_duration_in_milliseconds: The amount of time to
     wait after completing an upgrade domain before applying health policies.
     It is first interpreted as a string representing an ISO 8601 duration. If
     that fails, then it is interpreted as a number representing the total
     number of milliseconds.
    :type health_check_wait_duration_in_milliseconds: str
    :param health_check_stable_duration_in_milliseconds: The amount of time
     that the application or cluster must remain healthy before the upgrade
     proceeds to the next upgrade domain. It is first interpreted as a string
     representing an ISO 8601 duration. If that fails, then it is interpreted
     as a number representing the total number of milliseconds.
    :type health_check_stable_duration_in_milliseconds: str
    :param health_check_retry_timeout_in_milliseconds: The amount of time to
     retry health evaluation when the application or cluster is unhealthy
     before FailureAction is executed. It is first interpreted as a string
     representing an ISO 8601 duration. If that fails, then it is interpreted
     as a number representing the total number of milliseconds.
    :type health_check_retry_timeout_in_milliseconds: str
    :param upgrade_timeout_in_milliseconds: The amount of time the overall
     upgrade has to complete before FailureAction is executed. It is first
     interpreted as a string representing an ISO 8601 duration. If that fails,
     then it is interpreted as a number representing the total number of
     milliseconds.
    :type upgrade_timeout_in_milliseconds: str
    :param upgrade_domain_timeout_in_milliseconds: The amount of time each
     upgrade domain has to complete before FailureAction is executed. It is
     first interpreted as a string representing an ISO 8601 duration. If that
     fails, then it is interpreted as a number representing the total number of
     milliseconds.
    :type upgrade_domain_timeout_in_milliseconds: str
    :param instance_close_delay_duration_in_seconds: Duration in seconds, to
     wait before a stateless instance is closed, to allow the active requests
     to drain gracefully. This would be effective when the instance is closing
     during the application/cluster
     upgrade, only for those instances which have a non-zero delay duration
     configured in the service description. See
     InstanceCloseDelayDurationSeconds property in $ref:
     "#/definitions/StatelessServiceDescription.yaml" for details.
     Note, the default value of InstanceCloseDelayDurationInSeconds is
     4294967295, which indicates that the behavior will entirely depend on the
     delay configured in the stateless service description.
    :type instance_close_delay_duration_in_seconds: long
    """

    _validation = {
        'rolling_upgrade_mode': {'required': True},
    }

    _attribute_map = {
        'rolling_upgrade_mode': {'key': 'RollingUpgradeMode', 'type': 'str'},
        'force_restart': {'key': 'ForceRestart', 'type': 'bool'},
        'replica_set_check_timeout_in_milliseconds': {'key': 'ReplicaSetCheckTimeoutInMilliseconds', 'type': 'long'},
        'failure_action': {'key': 'FailureAction', 'type': 'str'},
        'health_check_wait_duration_in_milliseconds': {'key': 'HealthCheckWaitDurationInMilliseconds', 'type': 'str'},
        'health_check_stable_duration_in_milliseconds': {'key': 'HealthCheckStableDurationInMilliseconds', 'type': 'str'},
        'health_check_retry_timeout_in_milliseconds': {'key': 'HealthCheckRetryTimeoutInMilliseconds', 'type': 'str'},
        'upgrade_timeout_in_milliseconds': {'key': 'UpgradeTimeoutInMilliseconds', 'type': 'str'},
        'upgrade_domain_timeout_in_milliseconds': {'key': 'UpgradeDomainTimeoutInMilliseconds', 'type': 'str'},
        'instance_close_delay_duration_in_seconds': {'key': 'InstanceCloseDelayDurationInSeconds', 'type': 'long'},
    }

    def __init__(self, **kwargs):
        super(RollingUpgradeUpdateDescription, self).__init__(**kwargs)
        self.rolling_upgrade_mode = kwargs.get('rolling_upgrade_mode', "UnmonitoredAuto")
        self.force_restart = kwargs.get('force_restart', None)
        self.replica_set_check_timeout_in_milliseconds = kwargs.get('replica_set_check_timeout_in_milliseconds', None)
        self.failure_action = kwargs.get('failure_action', None)
        self.health_check_wait_duration_in_milliseconds = kwargs.get('health_check_wait_duration_in_milliseconds', None)
        self.health_check_stable_duration_in_milliseconds = kwargs.get('health_check_stable_duration_in_milliseconds', None)
        self.health_check_retry_timeout_in_milliseconds = kwargs.get('health_check_retry_timeout_in_milliseconds', None)
        self.upgrade_timeout_in_milliseconds = kwargs.get('upgrade_timeout_in_milliseconds', None)
        self.upgrade_domain_timeout_in_milliseconds = kwargs.get('upgrade_domain_timeout_in_milliseconds', None)
        self.instance_close_delay_duration_in_seconds = kwargs.get('instance_close_delay_duration_in_seconds', None)
