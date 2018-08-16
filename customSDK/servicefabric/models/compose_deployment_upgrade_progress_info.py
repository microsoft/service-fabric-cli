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


class ComposeDeploymentUpgradeProgressInfo(Model):
    """Describes the parameters for a compose deployment upgrade.

    :param deployment_name: The name of the target deployment.
    :type deployment_name: str
    :param application_name: The name of the target application, including the
     'fabric:' URI scheme.
    :type application_name: str
    :param upgrade_state: The state of the compose deployment upgrade.
     Possible values include: 'Invalid', 'ProvisioningTarget',
     'RollingForwardInProgress', 'RollingForwardPending',
     'UnprovisioningCurrent', 'RollingForwardCompleted',
     'RollingBackInProgress', 'UnprovisioningTarget', 'RollingBackCompleted',
     'Failed'
    :type upgrade_state: str or
     ~azure.servicefabric.models.ComposeDeploymentUpgradeState
    :param upgrade_status_details: Additional detailed information about the
     status of the pending upgrade.
    :type upgrade_status_details: str
    :param upgrade_kind: The kind of upgrade out of the following possible
     values. Possible values include: 'Invalid', 'Rolling'. Default value:
     "Rolling" .
    :type upgrade_kind: str or ~azure.servicefabric.models.UpgradeKind
    :param rolling_upgrade_mode: The mode used to monitor health during a
     rolling upgrade. The values are UnmonitoredAuto, UnmonitoredManual, and
     Monitored. Possible values include: 'Invalid', 'UnmonitoredAuto',
     'UnmonitoredManual', 'Monitored'. Default value: "UnmonitoredAuto" .
    :type rolling_upgrade_mode: str or ~azure.servicefabric.models.UpgradeMode
    :param force_restart: If true, then processes are forcefully restarted
     during upgrade even when the code version has not changed (the upgrade
     only changes configuration or data).
    :type force_restart: bool
    :param upgrade_replica_set_check_timeout_in_seconds: The maximum amount of
     time to block processing of an upgrade domain and prevent loss of
     availability when there are unexpected issues. When this timeout expires,
     processing of the upgrade domain will proceed regardless of availability
     loss issues. The timeout is reset at the start of each upgrade domain.
     Valid values are between 0 and 42949672925 inclusive. (unsigned 32-bit
     integer).
    :type upgrade_replica_set_check_timeout_in_seconds: long
    :param monitoring_policy: Describes the parameters for monitoring an
     upgrade in Monitored mode.
    :type monitoring_policy:
     ~azure.servicefabric.models.MonitoringPolicyDescription
    :param application_health_policy: Defines a health policy used to evaluate
     the health of an application or one of its children entities.
    :type application_health_policy:
     ~azure.servicefabric.models.ApplicationHealthPolicy
    :param target_application_type_version: The target application type
     version (found in the application manifest) for the application upgrade.
    :type target_application_type_version: str
    :param upgrade_duration: The estimated amount of time that the overall
     upgrade elapsed. It is first interpreted as a string representing an ISO
     8601 duration. If that fails, then it is interpreted as a number
     representing the total number of milliseconds.
    :type upgrade_duration: str
    :param current_upgrade_domain_duration: The estimated amount of time spent
     processing current Upgrade Domain. It is first interpreted as a string
     representing an ISO 8601 duration. If that fails, then it is interpreted
     as a number representing the total number of milliseconds.
    :type current_upgrade_domain_duration: str
    :param application_unhealthy_evaluations: List of health evaluations that
     resulted in the current aggregated health state.
    :type application_unhealthy_evaluations:
     list[~azure.servicefabric.models.HealthEvaluationWrapper]
    :param current_upgrade_domain_progress: Information about the current
     in-progress upgrade domain.
    :type current_upgrade_domain_progress:
     ~azure.servicefabric.models.CurrentUpgradeDomainProgressInfo
    :param start_timestamp_utc: The estimated UTC datetime when the upgrade
     started.
    :type start_timestamp_utc: str
    :param failure_timestamp_utc: The estimated UTC datetime when the upgrade
     failed and FailureAction was executed.
    :type failure_timestamp_utc: str
    :param failure_reason: The cause of an upgrade failure that resulted in
     FailureAction being executed. Possible values include: 'None',
     'Interrupted', 'HealthCheck', 'UpgradeDomainTimeout',
     'OverallUpgradeTimeout'
    :type failure_reason: str or ~azure.servicefabric.models.FailureReason
    :param upgrade_domain_progress_at_failure: Information about the upgrade
     domain progress at the time of upgrade failure.
    :type upgrade_domain_progress_at_failure:
     ~azure.servicefabric.models.FailureUpgradeDomainProgressInfo
    :param application_upgrade_status_details: Additional details of
     application upgrade including failure message.
    :type application_upgrade_status_details: str
    """

    _attribute_map = {
        'deployment_name': {'key': 'DeploymentName', 'type': 'str'},
        'application_name': {'key': 'ApplicationName', 'type': 'str'},
        'upgrade_state': {'key': 'UpgradeState', 'type': 'str'},
        'upgrade_status_details': {'key': 'UpgradeStatusDetails', 'type': 'str'},
        'upgrade_kind': {'key': 'UpgradeKind', 'type': 'str'},
        'rolling_upgrade_mode': {'key': 'RollingUpgradeMode', 'type': 'str'},
        'force_restart': {'key': 'ForceRestart', 'type': 'bool'},
        'upgrade_replica_set_check_timeout_in_seconds': {'key': 'UpgradeReplicaSetCheckTimeoutInSeconds', 'type': 'long'},
        'monitoring_policy': {'key': 'MonitoringPolicy', 'type': 'MonitoringPolicyDescription'},
        'application_health_policy': {'key': 'ApplicationHealthPolicy', 'type': 'ApplicationHealthPolicy'},
        'target_application_type_version': {'key': 'TargetApplicationTypeVersion', 'type': 'str'},
        'upgrade_duration': {'key': 'UpgradeDuration', 'type': 'str'},
        'current_upgrade_domain_duration': {'key': 'CurrentUpgradeDomainDuration', 'type': 'str'},
        'application_unhealthy_evaluations': {'key': 'ApplicationUnhealthyEvaluations', 'type': '[HealthEvaluationWrapper]'},
        'current_upgrade_domain_progress': {'key': 'CurrentUpgradeDomainProgress', 'type': 'CurrentUpgradeDomainProgressInfo'},
        'start_timestamp_utc': {'key': 'StartTimestampUtc', 'type': 'str'},
        'failure_timestamp_utc': {'key': 'FailureTimestampUtc', 'type': 'str'},
        'failure_reason': {'key': 'FailureReason', 'type': 'str'},
        'upgrade_domain_progress_at_failure': {'key': 'UpgradeDomainProgressAtFailure', 'type': 'FailureUpgradeDomainProgressInfo'},
        'application_upgrade_status_details': {'key': 'ApplicationUpgradeStatusDetails', 'type': 'str'},
    }

    def __init__(self, deployment_name=None, application_name=None, upgrade_state=None, upgrade_status_details=None, upgrade_kind="Rolling", rolling_upgrade_mode="UnmonitoredAuto", force_restart=None, upgrade_replica_set_check_timeout_in_seconds=None, monitoring_policy=None, application_health_policy=None, target_application_type_version=None, upgrade_duration=None, current_upgrade_domain_duration=None, application_unhealthy_evaluations=None, current_upgrade_domain_progress=None, start_timestamp_utc=None, failure_timestamp_utc=None, failure_reason=None, upgrade_domain_progress_at_failure=None, application_upgrade_status_details=None):
        super(ComposeDeploymentUpgradeProgressInfo, self).__init__()
        self.deployment_name = deployment_name
        self.application_name = application_name
        self.upgrade_state = upgrade_state
        self.upgrade_status_details = upgrade_status_details
        self.upgrade_kind = upgrade_kind
        self.rolling_upgrade_mode = rolling_upgrade_mode
        self.force_restart = force_restart
        self.upgrade_replica_set_check_timeout_in_seconds = upgrade_replica_set_check_timeout_in_seconds
        self.monitoring_policy = monitoring_policy
        self.application_health_policy = application_health_policy
        self.target_application_type_version = target_application_type_version
        self.upgrade_duration = upgrade_duration
        self.current_upgrade_domain_duration = current_upgrade_domain_duration
        self.application_unhealthy_evaluations = application_unhealthy_evaluations
        self.current_upgrade_domain_progress = current_upgrade_domain_progress
        self.start_timestamp_utc = start_timestamp_utc
        self.failure_timestamp_utc = failure_timestamp_utc
        self.failure_reason = failure_reason
        self.upgrade_domain_progress_at_failure = upgrade_domain_progress_at_failure
        self.application_upgrade_status_details = application_upgrade_status_details
