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

from enum import Enum


class HealthState(Enum):

    invalid = "Invalid"
    ok = "Ok"
    warning = "Warning"
    error = "Error"
    unknown = "Unknown"


class FabricErrorCodes(Enum):

    fabric_e_invalid_partition_key = "FABRIC_E_INVALID_PARTITION_KEY"
    fabric_e_imagebuilder_validation_error = "FABRIC_E_IMAGEBUILDER_VALIDATION_ERROR"
    fabric_e_invalid_address = "FABRIC_E_INVALID_ADDRESS"
    fabric_e_application_not_upgrading = "FABRIC_E_APPLICATION_NOT_UPGRADING"
    fabric_e_application_upgrade_validation_error = "FABRIC_E_APPLICATION_UPGRADE_VALIDATION_ERROR"
    fabric_e_fabric_not_upgrading = "FABRIC_E_FABRIC_NOT_UPGRADING"
    fabric_e_fabric_upgrade_validation_error = "FABRIC_E_FABRIC_UPGRADE_VALIDATION_ERROR"
    fabric_e_invalid_configuration = "FABRIC_E_INVALID_CONFIGURATION"
    fabric_e_invalid_name_uri = "FABRIC_E_INVALID_NAME_URI"
    fabric_e_path_too_long = "FABRIC_E_PATH_TOO_LONG"
    fabric_e_key_too_large = "FABRIC_E_KEY_TOO_LARGE"
    fabric_e_service_affinity_chain_not_supported = "FABRIC_E_SERVICE_AFFINITY_CHAIN_NOT_SUPPORTED"
    fabric_e_invalid_atomic_group = "FABRIC_E_INVALID_ATOMIC_GROUP"
    fabric_e_value_empty = "FABRIC_E_VALUE_EMPTY"
    fabric_e_node_not_found = "FABRIC_E_NODE_NOT_FOUND"
    fabric_e_application_type_not_found = "FABRIC_E_APPLICATION_TYPE_NOT_FOUND"
    fabric_e_application_not_found = "FABRIC_E_APPLICATION_NOT_FOUND"
    fabric_e_service_type_not_found = "FABRIC_E_SERVICE_TYPE_NOT_FOUND"
    fabric_e_service_does_not_exist = "FABRIC_E_SERVICE_DOES_NOT_EXIST"
    fabric_e_service_type_template_not_found = "FABRIC_E_SERVICE_TYPE_TEMPLATE_NOT_FOUND"
    fabric_e_configuration_section_not_found = "FABRIC_E_CONFIGURATION_SECTION_NOT_FOUND"
    fabric_e_partition_not_found = "FABRIC_E_PARTITION_NOT_FOUND"
    fabric_e_replica_does_not_exist = "FABRIC_E_REPLICA_DOES_NOT_EXIST"
    fabric_e_service_group_does_not_exist = "FABRIC_E_SERVICE_GROUP_DOES_NOT_EXIST"
    fabric_e_configuration_parameter_not_found = "FABRIC_E_CONFIGURATION_PARAMETER_NOT_FOUND"
    fabric_e_directory_not_found = "FABRIC_E_DIRECTORY_NOT_FOUND"
    fabric_e_fabric_version_not_found = "FABRIC_E_FABRIC_VERSION_NOT_FOUND"
    fabric_e_file_not_found = "FABRIC_E_FILE_NOT_FOUND"
    fabric_e_name_does_not_exist = "FABRIC_E_NAME_DOES_NOT_EXIST"
    fabric_e_property_does_not_exist = "FABRIC_E_PROPERTY_DOES_NOT_EXIST"
    fabric_e_enumeration_completed = "FABRIC_E_ENUMERATION_COMPLETED"
    fabric_e_service_manifest_not_found = "FABRIC_E_SERVICE_MANIFEST_NOT_FOUND"
    fabric_e_key_not_found = "FABRIC_E_KEY_NOT_FOUND"
    fabric_e_health_entity_not_found = "FABRIC_E_HEALTH_ENTITY_NOT_FOUND"
    fabric_e_application_type_already_exists = "FABRIC_E_APPLICATION_TYPE_ALREADY_EXISTS"
    fabric_e_application_already_exists = "FABRIC_E_APPLICATION_ALREADY_EXISTS"
    fabric_e_application_already_in_target_version = "FABRIC_E_APPLICATION_ALREADY_IN_TARGET_VERSION"
    fabric_e_application_type_provision_in_progress = "FABRIC_E_APPLICATION_TYPE_PROVISION_IN_PROGRESS"
    fabric_e_application_upgrade_in_progress = "FABRIC_E_APPLICATION_UPGRADE_IN_PROGRESS"
    fabric_e_service_already_exists = "FABRIC_E_SERVICE_ALREADY_EXISTS"
    fabric_e_service_group_already_exists = "FABRIC_E_SERVICE_GROUP_ALREADY_EXISTS"
    fabric_e_application_type_in_use = "FABRIC_E_APPLICATION_TYPE_IN_USE"
    fabric_e_fabric_already_in_target_version = "FABRIC_E_FABRIC_ALREADY_IN_TARGET_VERSION"
    fabric_e_fabric_version_already_exists = "FABRIC_E_FABRIC_VERSION_ALREADY_EXISTS"
    fabric_e_fabric_version_in_use = "FABRIC_E_FABRIC_VERSION_IN_USE"
    fabric_e_fabric_upgrade_in_progress = "FABRIC_E_FABRIC_UPGRADE_IN_PROGRESS"
    fabric_e_name_already_exists = "FABRIC_E_NAME_ALREADY_EXISTS"
    fabric_e_name_not_empty = "FABRIC_E_NAME_NOT_EMPTY"
    fabric_e_property_check_failed = "FABRIC_E_PROPERTY_CHECK_FAILED"
    fabric_e_service_metadata_mismatch = "FABRIC_E_SERVICE_METADATA_MISMATCH"
    fabric_e_service_type_mismatch = "FABRIC_E_SERVICE_TYPE_MISMATCH"
    fabric_e_health_stale_report = "FABRIC_E_HEALTH_STALE_REPORT"
    fabric_e_sequence_number_check_failed = "FABRIC_E_SEQUENCE_NUMBER_CHECK_FAILED"
    fabric_e_node_has_not_stopped_yet = "FABRIC_E_NODE_HAS_NOT_STOPPED_YET"
    fabric_e_instance_id_mismatch = "FABRIC_E_INSTANCE_ID_MISMATCH"
    fabric_e_value_too_large = "FABRIC_E_VALUE_TOO_LARGE"
    fabric_e_no_write_quorum = "FABRIC_E_NO_WRITE_QUORUM"
    fabric_e_not_primary = "FABRIC_E_NOT_PRIMARY"
    fabric_e_not_ready = "FABRIC_E_NOT_READY"
    fabric_e_reconfiguration_pending = "FABRIC_E_RECONFIGURATION_PENDING"
    fabric_e_service_offline = "FABRIC_E_SERVICE_OFFLINE"
    e_abort = "E_ABORT"
    fabric_e_communication_error = "FABRIC_E_COMMUNICATION_ERROR"
    fabric_e_operation_not_complete = "FABRIC_E_OPERATION_NOT_COMPLETE"
    fabric_e_timeout = "FABRIC_E_TIMEOUT"
    fabric_e_node_is_up = "FABRIC_E_NODE_IS_UP"
    e_fail = "E_FAIL"
    fabric_e_backup_is_enabled = "FABRIC_E_BACKUP_IS_ENABLED"
    fabric_e_restore_source_target_partition_mismatch = "FABRIC_E_RESTORE_SOURCE_TARGET_PARTITION_MISMATCH"
    fabric_e_invalid_for_stateless_services = "FABRIC_E_INVALID_FOR_STATELESS_SERVICES"
    fabric_e_backup_not_enabled = "FABRIC_E_BACKUP_NOT_ENABLED"
    fabric_e_backup_policy_not_existing = "FABRIC_E_BACKUP_POLICY_NOT_EXISTING"
    fabric_e_fault_analysis_service_not_existing = "FABRIC_E_FAULT_ANALYSIS_SERVICE_NOT_EXISTING"
    fabric_e_backup_in_progress = "FABRIC_E_BACKUP_IN_PROGRESS"
    fabric_e_restore_in_progress = "FABRIC_E_RESTORE_IN_PROGRESS"
    fabric_e_backup_policy_already_existing = "FABRIC_E_BACKUP_POLICY_ALREADY_EXISTING"
    fabric_e_invalid_service_scaling_policy = "FABRIC_E_INVALID_SERVICE_SCALING_POLICY"
    e_invalidarg = "E_INVALIDARG"
    fabric_e_single_instance_application_already_exists = "FABRIC_E_SINGLE_INSTANCE_APPLICATION_ALREADY_EXISTS"
    fabric_e_single_instance_application_not_found = "FABRIC_E_SINGLE_INSTANCE_APPLICATION_NOT_FOUND"
    fabric_e_volume_already_exists = "FABRIC_E_VOLUME_ALREADY_EXISTS"
    fabric_e_volume_not_found = "FABRIC_E_VOLUME_NOT_FOUND"
    serialization_error = "SerializationError"
    fabric_e_imagebuilder_reserved_directory_error = "FABRIC_E_IMAGEBUILDER_RESERVED_DIRECTORY_ERROR"


class ApplicationDefinitionKind(Enum):

    invalid = "Invalid"
    service_fabric_application_description = "ServiceFabricApplicationDescription"
    compose = "Compose"


class ApplicationStatus(Enum):

    invalid = "Invalid"
    ready = "Ready"
    upgrading = "Upgrading"
    creating = "Creating"
    deleting = "Deleting"
    failed = "Failed"


class ApplicationPackageCleanupPolicy(Enum):

    invalid = "Invalid"
    default = "Default"
    automatic = "Automatic"
    manual = "Manual"


class ApplicationTypeDefinitionKind(Enum):

    invalid = "Invalid"
    service_fabric_application_package = "ServiceFabricApplicationPackage"
    compose = "Compose"


class ApplicationTypeStatus(Enum):

    invalid = "Invalid"
    provisioning = "Provisioning"
    available = "Available"
    unprovisioning = "Unprovisioning"
    failed = "Failed"


class UpgradeKind(Enum):

    invalid = "Invalid"
    rolling = "Rolling"


class UpgradeMode(Enum):

    invalid = "Invalid"
    unmonitored_auto = "UnmonitoredAuto"
    unmonitored_manual = "UnmonitoredManual"
    monitored = "Monitored"


class FailureAction(Enum):

    invalid = "Invalid"
    rollback = "Rollback"
    manual = "Manual"


class UpgradeDomainState(Enum):

    invalid = "Invalid"
    pending = "Pending"
    in_progress = "InProgress"
    completed = "Completed"


class UpgradeState(Enum):

    invalid = "Invalid"
    rolling_back_in_progress = "RollingBackInProgress"
    rolling_back_completed = "RollingBackCompleted"
    rolling_forward_pending = "RollingForwardPending"
    rolling_forward_in_progress = "RollingForwardInProgress"
    rolling_forward_completed = "RollingForwardCompleted"
    failed = "Failed"


class NodeUpgradePhase(Enum):

    invalid = "Invalid"
    pre_upgrade_safety_check = "PreUpgradeSafetyCheck"
    upgrading = "Upgrading"
    post_upgrade_safety_check = "PostUpgradeSafetyCheck"


class FailureReason(Enum):

    none = "None"
    interrupted = "Interrupted"
    health_check = "HealthCheck"
    upgrade_domain_timeout = "UpgradeDomainTimeout"
    overall_upgrade_timeout = "OverallUpgradeTimeout"


class DeactivationIntent(Enum):

    pause = "Pause"
    restart = "Restart"
    remove_data = "RemoveData"


class DeployedApplicationStatus(Enum):

    invalid = "Invalid"
    downloading = "Downloading"
    activating = "Activating"
    active = "Active"
    upgrading = "Upgrading"
    deactivating = "Deactivating"


class ReplicaStatus(Enum):

    invalid = "Invalid"
    in_build = "InBuild"
    standby = "Standby"
    ready = "Ready"
    down = "Down"
    dropped = "Dropped"


class ReplicaRole(Enum):

    unknown = "Unknown"
    none = "None"
    primary = "Primary"
    idle_secondary = "IdleSecondary"
    active_secondary = "ActiveSecondary"


class ReconfigurationPhase(Enum):

    unknown = "Unknown"
    none = "None"
    phase0 = "Phase0"
    phase1 = "Phase1"
    phase2 = "Phase2"
    phase3 = "Phase3"
    phase4 = "Phase4"
    abort_phase_zero = "AbortPhaseZero"


class ReconfigurationType(Enum):

    unknown = "Unknown"
    swap_primary = "SwapPrimary"
    failover = "Failover"
    other = "Other"


class EntityKind(Enum):

    invalid = "Invalid"
    node = "Node"
    partition = "Partition"
    service = "Service"
    application = "Application"
    replica = "Replica"
    deployed_application = "DeployedApplication"
    deployed_service_package = "DeployedServicePackage"
    cluster = "Cluster"


class FabricEventKind(Enum):

    cluster_event = "ClusterEvent"
    container_instance_event = "ContainerInstanceEvent"
    node_event = "NodeEvent"
    application_event = "ApplicationEvent"
    service_event = "ServiceEvent"
    partition_event = "PartitionEvent"
    replica_event = "ReplicaEvent"
    partition_analysis_event = "PartitionAnalysisEvent"
    application_created = "ApplicationCreated"
    application_deleted = "ApplicationDeleted"
    application_new_health_report = "ApplicationNewHealthReport"
    application_health_report_expired = "ApplicationHealthReportExpired"
    application_upgrade_completed = "ApplicationUpgradeCompleted"
    application_upgrade_domain_completed = "ApplicationUpgradeDomainCompleted"
    application_upgrade_rollback_completed = "ApplicationUpgradeRollbackCompleted"
    application_upgrade_rollback_started = "ApplicationUpgradeRollbackStarted"
    application_upgrade_started = "ApplicationUpgradeStarted"
    deployed_application_new_health_report = "DeployedApplicationNewHealthReport"
    deployed_application_health_report_expired = "DeployedApplicationHealthReportExpired"
    application_process_exited = "ApplicationProcessExited"
    application_container_instance_exited = "ApplicationContainerInstanceExited"
    node_aborted = "NodeAborted"
    node_added_to_cluster = "NodeAddedToCluster"
    node_closed = "NodeClosed"
    node_deactivate_completed = "NodeDeactivateCompleted"
    node_deactivate_started = "NodeDeactivateStarted"
    node_down = "NodeDown"
    node_new_health_report = "NodeNewHealthReport"
    node_health_report_expired = "NodeHealthReportExpired"
    node_open_succeeded = "NodeOpenSucceeded"
    node_open_failed = "NodeOpenFailed"
    node_removed_from_cluster = "NodeRemovedFromCluster"
    node_up = "NodeUp"
    partition_new_health_report = "PartitionNewHealthReport"
    partition_health_report_expired = "PartitionHealthReportExpired"
    partition_reconfigured = "PartitionReconfigured"
    partition_primary_move_analysis = "PartitionPrimaryMoveAnalysis"
    service_created = "ServiceCreated"
    service_deleted = "ServiceDeleted"
    service_new_health_report = "ServiceNewHealthReport"
    service_health_report_expired = "ServiceHealthReportExpired"
    deployed_service_package_new_health_report = "DeployedServicePackageNewHealthReport"
    deployed_service_package_health_report_expired = "DeployedServicePackageHealthReportExpired"
    stateful_replica_new_health_report = "StatefulReplicaNewHealthReport"
    stateful_replica_health_report_expired = "StatefulReplicaHealthReportExpired"
    stateless_replica_new_health_report = "StatelessReplicaNewHealthReport"
    stateless_replica_health_report_expired = "StatelessReplicaHealthReportExpired"
    cluster_new_health_report = "ClusterNewHealthReport"
    cluster_health_report_expired = "ClusterHealthReportExpired"
    cluster_upgrade_completed = "ClusterUpgradeCompleted"
    cluster_upgrade_domain_completed = "ClusterUpgradeDomainCompleted"
    cluster_upgrade_rollback_completed = "ClusterUpgradeRollbackCompleted"
    cluster_upgrade_rollback_started = "ClusterUpgradeRollbackStarted"
    cluster_upgrade_started = "ClusterUpgradeStarted"
    chaos_stopped = "ChaosStopped"
    chaos_started = "ChaosStarted"
    chaos_code_package_restart_scheduled = "ChaosCodePackageRestartScheduled"
    chaos_replica_removal_scheduled = "ChaosReplicaRemovalScheduled"
    chaos_partition_secondary_move_scheduled = "ChaosPartitionSecondaryMoveScheduled"
    chaos_partition_primary_move_scheduled = "ChaosPartitionPrimaryMoveScheduled"
    chaos_replica_restart_scheduled = "ChaosReplicaRestartScheduled"
    chaos_node_restart_scheduled = "ChaosNodeRestartScheduled"


class HealthEvaluationKind(Enum):

    invalid = "Invalid"
    event = "Event"
    replicas = "Replicas"
    partitions = "Partitions"
    deployed_service_packages = "DeployedServicePackages"
    deployed_applications = "DeployedApplications"
    services = "Services"
    nodes = "Nodes"
    applications = "Applications"
    system_application = "SystemApplication"
    upgrade_domain_deployed_applications = "UpgradeDomainDeployedApplications"
    upgrade_domain_nodes = "UpgradeDomainNodes"
    replica = "Replica"
    partition = "Partition"
    deployed_service_package = "DeployedServicePackage"
    deployed_application = "DeployedApplication"
    service = "Service"
    node = "Node"
    application = "Application"
    delta_nodes_check = "DeltaNodesCheck"
    upgrade_domain_delta_nodes_check = "UpgradeDomainDeltaNodesCheck"
    application_type_applications = "ApplicationTypeApplications"


class NodeDeactivationIntent(Enum):

    invalid = "Invalid"
    pause = "Pause"
    restart = "Restart"
    remove_data = "RemoveData"
    remove_node = "RemoveNode"


class NodeDeactivationStatus(Enum):

    none = "None"
    safety_check_in_progress = "SafetyCheckInProgress"
    safety_check_complete = "SafetyCheckComplete"
    completed = "Completed"


class NodeDeactivationTaskType(Enum):

    invalid = "Invalid"
    infrastructure = "Infrastructure"
    repair = "Repair"
    client = "Client"


class NodeStatus(Enum):

    invalid = "Invalid"
    up = "Up"
    down = "Down"
    enabling = "Enabling"
    disabling = "Disabling"
    disabled = "Disabled"
    unknown = "Unknown"
    removed = "Removed"


class ServicePartitionStatus(Enum):

    invalid = "Invalid"
    ready = "Ready"
    not_ready = "NotReady"
    in_quorum_loss = "InQuorumLoss"
    reconfiguring = "Reconfiguring"
    deleting = "Deleting"


class ServiceStatus(Enum):

    unknown = "Unknown"
    active = "Active"
    upgrading = "Upgrading"
    deleting = "Deleting"
    creating = "Creating"
    failed = "Failed"


class ProvisionApplicationTypeKind(Enum):

    invalid = "Invalid"
    image_store_path = "ImageStorePath"
    external_store = "ExternalStore"


class UpgradeType(Enum):

    invalid = "Invalid"
    rolling = "Rolling"
    rolling_force_restart = "Rolling_ForceRestart"


class SafetyCheckKind(Enum):

    invalid = "Invalid"
    ensure_seed_node_quorum = "EnsureSeedNodeQuorum"
    ensure_partition_quorum = "EnsurePartitionQuorum"
    wait_for_primary_placement = "WaitForPrimaryPlacement"
    wait_for_primary_swap = "WaitForPrimarySwap"
    wait_for_reconfiguration = "WaitForReconfiguration"
    wait_for_inbuild_replica = "WaitForInbuildReplica"
    ensure_availability = "EnsureAvailability"


class CreateFabricDump(Enum):

    false = "False"
    true = "True"


class ServicePackageActivationMode(Enum):

    shared_process = "SharedProcess"
    exclusive_process = "ExclusiveProcess"


class ServiceKind(Enum):

    invalid = "Invalid"
    stateless = "Stateless"
    stateful = "Stateful"


class ServicePartitionKind(Enum):

    invalid = "Invalid"
    singleton = "Singleton"
    int64_range = "Int64Range"
    named = "Named"


class ServicePlacementPolicyType(Enum):

    invalid = "Invalid"
    invalid_domain = "InvalidDomain"
    required_domain = "RequiredDomain"
    preferred_primary_domain = "PreferredPrimaryDomain"
    required_domain_distribution = "RequiredDomainDistribution"
    non_partially_place_service = "NonPartiallyPlaceService"


class ServiceLoadMetricWeight(Enum):

    zero = "Zero"
    low = "Low"
    medium = "Medium"
    high = "High"


class HostType(Enum):

    invalid = "Invalid"
    exe_host = "ExeHost"
    container_host = "ContainerHost"


class HostIsolationMode(Enum):

    none = "None"
    process = "Process"
    hyper_v = "HyperV"


class DeploymentStatus(Enum):

    invalid = "Invalid"
    downloading = "Downloading"
    activating = "Activating"
    active = "Active"
    upgrading = "Upgrading"
    deactivating = "Deactivating"


class EntryPointStatus(Enum):

    invalid = "Invalid"
    pending = "Pending"
    starting = "Starting"
    started = "Started"
    stopping = "Stopping"
    stopped = "Stopped"


class ChaosStatus(Enum):

    invalid = "Invalid"
    running = "Running"
    stopped = "Stopped"


class ChaosScheduleStatus(Enum):

    invalid = "Invalid"
    stopped = "Stopped"
    active = "Active"
    expired = "Expired"
    pending = "Pending"


class ChaosEventKind(Enum):

    invalid = "Invalid"
    started = "Started"
    executing_faults = "ExecutingFaults"
    waiting = "Waiting"
    validation_failed = "ValidationFailed"
    test_error = "TestError"
    stopped = "Stopped"


class ComposeDeploymentStatus(Enum):

    invalid = "Invalid"
    provisioning = "Provisioning"
    creating = "Creating"
    ready = "Ready"
    unprovisioning = "Unprovisioning"
    deleting = "Deleting"
    failed = "Failed"
    upgrading = "Upgrading"


class ComposeDeploymentUpgradeState(Enum):

    invalid = "Invalid"
    provisioning_target = "ProvisioningTarget"
    rolling_forward_in_progress = "RollingForwardInProgress"
    rolling_forward_pending = "RollingForwardPending"
    unprovisioning_current = "UnprovisioningCurrent"
    rolling_forward_completed = "RollingForwardCompleted"
    rolling_back_in_progress = "RollingBackInProgress"
    unprovisioning_target = "UnprovisioningTarget"
    rolling_back_completed = "RollingBackCompleted"
    failed = "Failed"


class ServiceCorrelationScheme(Enum):

    invalid = "Invalid"
    affinity = "Affinity"
    aligned_affinity = "AlignedAffinity"
    non_aligned_affinity = "NonAlignedAffinity"


class MoveCost(Enum):

    zero = "Zero"
    low = "Low"
    medium = "Medium"
    high = "High"


class PartitionScheme(Enum):

    invalid = "Invalid"
    singleton = "Singleton"
    uniform_int64_range = "UniformInt64Range"
    named = "Named"


class ServiceOperationName(Enum):

    unknown = "Unknown"
    none = "None"
    open = "Open"
    change_role = "ChangeRole"
    close = "Close"
    abort = "Abort"


class ReplicatorOperationName(Enum):

    invalid = "Invalid"
    none = "None"
    open = "Open"
    change_role = "ChangeRole"
    update_epoch = "UpdateEpoch"
    close = "Close"
    abort = "Abort"
    on_data_loss = "OnDataLoss"
    wait_for_catchup = "WaitForCatchup"
    build = "Build"


class PartitionAccessStatus(Enum):

    invalid = "Invalid"
    granted = "Granted"
    reconfiguration_pending = "ReconfigurationPending"
    not_primary = "NotPrimary"
    no_write_quorum = "NoWriteQuorum"


class FabricReplicaStatus(Enum):

    invalid = "Invalid"
    down = "Down"
    up = "Up"


class ReplicaKind(Enum):

    invalid = "Invalid"
    key_value_store = "KeyValueStore"


class ServiceTypeRegistrationStatus(Enum):

    invalid = "Invalid"
    disabled = "Disabled"
    enabled = "Enabled"
    registered = "Registered"


class ServiceEndpointRole(Enum):

    invalid = "Invalid"
    stateless = "Stateless"
    stateful_primary = "StatefulPrimary"
    stateful_secondary = "StatefulSecondary"


class OperationState(Enum):

    invalid = "Invalid"
    running = "Running"
    rolling_back = "RollingBack"
    completed = "Completed"
    faulted = "Faulted"
    cancelled = "Cancelled"
    force_cancelled = "ForceCancelled"


class OperationType(Enum):

    invalid = "Invalid"
    partition_data_loss = "PartitionDataLoss"
    partition_quorum_loss = "PartitionQuorumLoss"
    partition_restart = "PartitionRestart"
    node_transition = "NodeTransition"


class PackageSharingPolicyScope(Enum):

    none = "None"
    all = "All"
    code = "Code"
    config = "Config"
    data = "Data"


class PropertyValueKind(Enum):

    invalid = "Invalid"
    binary = "Binary"
    int64 = "Int64"
    double = "Double"
    string = "String"
    guid = "Guid"


class PropertyBatchOperationKind(Enum):

    invalid = "Invalid"
    put = "Put"
    get = "Get"
    check_exists = "CheckExists"
    check_sequence = "CheckSequence"
    delete = "Delete"
    check_value = "CheckValue"


class PropertyBatchInfoKind(Enum):

    invalid = "Invalid"
    successful = "Successful"
    failed = "Failed"


class RetentionPolicyType(Enum):

    basic = "Basic"
    invalid = "Invalid"


class BackupStorageKind(Enum):

    invalid = "Invalid"
    file_share = "FileShare"
    azure_blob_store = "AzureBlobStore"


class BackupScheduleKind(Enum):

    invalid = "Invalid"
    time_based = "TimeBased"
    frequency_based = "FrequencyBased"


class BackupPolicyScope(Enum):

    invalid = "Invalid"
    partition = "Partition"
    service = "Service"
    application = "Application"


class BackupSuspensionScope(Enum):

    invalid = "Invalid"
    partition = "Partition"
    service = "Service"
    application = "Application"


class RestoreState(Enum):

    invalid = "Invalid"
    accepted = "Accepted"
    restore_in_progress = "RestoreInProgress"
    success = "Success"
    failure = "Failure"
    timeout = "Timeout"


class BackupType(Enum):

    invalid = "Invalid"
    full = "Full"
    incremental = "Incremental"


class BackupScheduleFrequencyType(Enum):

    invalid = "Invalid"
    daily = "Daily"
    weekly = "Weekly"


class DayOfWeek(Enum):

    sunday = "Sunday"
    monday = "Monday"
    tuesday = "Tuesday"
    wednesday = "Wednesday"
    thursday = "Thursday"
    friday = "Friday"
    saturday = "Saturday"


class BackupState(Enum):

    invalid = "Invalid"
    accepted = "Accepted"
    backup_in_progress = "BackupInProgress"
    success = "Success"
    failure = "Failure"
    timeout = "Timeout"


class BackupEntityKind(Enum):

    invalid = "Invalid"
    partition = "Partition"
    service = "Service"
    application = "Application"


class ImpactLevel(Enum):

    invalid = "Invalid"
    none = "None"
    restart = "Restart"
    remove_data = "RemoveData"
    remove_node = "RemoveNode"


class RepairImpactKind(Enum):

    invalid = "Invalid"
    node = "Node"


class RepairTargetKind(Enum):

    invalid = "Invalid"
    node = "Node"


class State(Enum):

    invalid = "Invalid"
    created = "Created"
    claimed = "Claimed"
    preparing = "Preparing"
    approved = "Approved"
    executing = "Executing"
    restoring = "Restoring"
    completed = "Completed"


class ResultStatus(Enum):

    invalid = "Invalid"
    succeeded = "Succeeded"
    cancelled = "Cancelled"
    interrupted = "Interrupted"
    failed = "Failed"
    pending = "Pending"


class RepairTaskHealthCheckState(Enum):

    not_started = "NotStarted"
    in_progress = "InProgress"
    succeeded = "Succeeded"
    skipped = "Skipped"
    timed_out = "TimedOut"


class ScalingTriggerKind(Enum):

    invalid = "Invalid"
    average_partition_load = "AveragePartitionLoad"
    average_service_load = "AverageServiceLoad"


class ScalingMechanismKind(Enum):

    invalid = "Invalid"
    partition_instance_count = "PartitionInstanceCount"
    add_remove_incremental_named_partition = "AddRemoveIncrementalNamedPartition"


class ResourceStatus(Enum):

    unknown = "Unknown"
    ready = "Ready"
    upgrading = "Upgrading"
    creating = "Creating"
    deleting = "Deleting"
    failed = "Failed"


class SecretKind(Enum):

    inlined_value = "inlinedValue"


class VolumeProvider(Enum):

    sf_azure_file = "SFAzureFile"


class SizeTypes(Enum):

    small = "Small"
    medium = "Medium"
    large = "Large"


class ApplicationScopedVolumeKind(Enum):

    service_fabric_volume_disk = "ServiceFabricVolumeDisk"


class NetworkKind(Enum):

    local = "Local"


class HeaderMatchType(Enum):

    exact = "exact"


class OperatingSystemType(Enum):

    linux = "Linux"
    windows = "Windows"


class DiagnosticsSinkKind(Enum):

    invalid = "Invalid"
    azure_internal_monitoring_pipeline = "AzureInternalMonitoringPipeline"


class AutoScalingMechanismKind(Enum):

    add_remove_replica = "AddRemoveReplica"


class AutoScalingMetricKind(Enum):

    resource = "Resource"


class AutoScalingResourceMetricName(Enum):

    cpu = "cpu"
    memory_in_gb = "memoryInGB"


class AutoScalingTriggerKind(Enum):

    average_load = "AverageLoad"


class NodeStatusFilter(Enum):

    default = "default"
    all = "all"
    up = "up"
    down = "down"
    enabling = "enabling"
    disabling = "disabling"
    disabled = "disabled"
    unknown = "unknown"
    removed = "removed"


class ReplicaHealthReportServiceKind(Enum):

    stateless = "Stateless"
    stateful = "Stateful"


class DataLossMode(Enum):

    invalid = "Invalid"
    partial_data_loss = "PartialDataLoss"
    full_data_loss = "FullDataLoss"


class NodeTransitionType(Enum):

    invalid = "Invalid"
    start = "Start"
    stop = "Stop"


class QuorumLossMode(Enum):

    invalid = "Invalid"
    quorum_replicas = "QuorumReplicas"
    all_replicas = "AllReplicas"


class RestartPartitionMode(Enum):

    invalid = "Invalid"
    all_replicas_or_instances = "AllReplicasOrInstances"
    only_active_secondaries = "OnlyActiveSecondaries"
