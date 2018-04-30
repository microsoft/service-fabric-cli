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


class ComposeDeploymentUpgradeDescription(Model):
    """Describes the parameters for a compose deployment upgrade.

    :param deployment_name: The name of the deployment.
    :type deployment_name: str
    :param compose_file_content: The content of the compose file that
     describes the deployment to create.
    :type compose_file_content: str
    :param registry_credential: Credential information to connect to container
     registry.
    :type registry_credential: ~azure.servicefabric.models.RegistryCredential
    :param upgrade_kind: The kind of upgrade out of the following possible
     values. Possible values include: 'Invalid', 'Rolling'. Default value:
     "Rolling" .
    :type upgrade_kind: str or ~azure.servicefabric.models.UpgradeKind
    :param rolling_upgrade_mode: The mode used to monitor health during a
     rolling upgrade. The values are UnmonitoredAuto, UnmonitoredManual, and
     Monitored. Possible values include: 'Invalid', 'UnmonitoredAuto',
     'UnmonitoredManual', 'Monitored'. Default value: "UnmonitoredAuto" .
    :type rolling_upgrade_mode: str or ~azure.servicefabric.models.UpgradeMode
    :param upgrade_replica_set_check_timeout_in_seconds: The maximum amount of
     time to block processing of an upgrade domain and prevent loss of
     availability when there are unexpected issues. When this timeout expires,
     processing of the upgrade domain will proceed regardless of availability
     loss issues. The timeout is reset at the start of each upgrade domain.
     Valid values are between 0 and 42949672925 inclusive. (unsigned 32-bit
     integer).
    :type upgrade_replica_set_check_timeout_in_seconds: long
    :param force_restart: If true, then processes are forcefully restarted
     during upgrade even when the code version has not changed (the upgrade
     only changes configuration or data).
    :type force_restart: bool
    :param monitoring_policy: Describes the parameters for monitoring an
     upgrade in Monitored mode.
    :type monitoring_policy:
     ~azure.servicefabric.models.MonitoringPolicyDescription
    :param application_health_policy: Defines a health policy used to evaluate
     the health of an application or one of its children entities.
    :type application_health_policy:
     ~azure.servicefabric.models.ApplicationHealthPolicy
    """

    _validation = {
        'deployment_name': {'required': True},
        'compose_file_content': {'required': True},
        'upgrade_kind': {'required': True},
    }

    _attribute_map = {
        'deployment_name': {'key': 'DeploymentName', 'type': 'str'},
        'compose_file_content': {'key': 'ComposeFileContent', 'type': 'str'},
        'registry_credential': {'key': 'RegistryCredential', 'type': 'RegistryCredential'},
        'upgrade_kind': {'key': 'UpgradeKind', 'type': 'str'},
        'rolling_upgrade_mode': {'key': 'RollingUpgradeMode', 'type': 'str'},
        'upgrade_replica_set_check_timeout_in_seconds': {'key': 'UpgradeReplicaSetCheckTimeoutInSeconds', 'type': 'long'},
        'force_restart': {'key': 'ForceRestart', 'type': 'bool'},
        'monitoring_policy': {'key': 'MonitoringPolicy', 'type': 'MonitoringPolicyDescription'},
        'application_health_policy': {'key': 'ApplicationHealthPolicy', 'type': 'ApplicationHealthPolicy'},
    }

    def __init__(self, deployment_name, compose_file_content, registry_credential=None, upgrade_kind="Rolling", rolling_upgrade_mode="UnmonitoredAuto", upgrade_replica_set_check_timeout_in_seconds=None, force_restart=None, monitoring_policy=None, application_health_policy=None):
        self.deployment_name = deployment_name
        self.compose_file_content = compose_file_content
        self.registry_credential = registry_credential
        self.upgrade_kind = upgrade_kind
        self.rolling_upgrade_mode = rolling_upgrade_mode
        self.upgrade_replica_set_check_timeout_in_seconds = upgrade_replica_set_check_timeout_in_seconds
        self.force_restart = force_restart
        self.monitoring_policy = monitoring_policy
        self.application_health_policy = application_health_policy
