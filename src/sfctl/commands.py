# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Command and help loader for the Service Fabric CLI.

Commands are stored as one to one mappings between command line syntax and
python function.
"""

from collections import OrderedDict
from knack.commands import CLICommandsLoader, CommandGroup
from knack.help import CLIHelp
from sfctl.apiclient import create as client_create

# Need to import so global help dict gets updated
import sfctl.helps.app  # pylint: disable=unused-import
import sfctl.helps.settings  # pylint: disable=unused-import
import sfctl.helps.main  # pylint: disable=unused-import
import sfctl.helps.health  # pylint: disable=unused-import
import sfctl.helps.cluster_upgrade  # pylint: disable=unused-import
import sfctl.helps.compose  # pylint: disable=unused-import
import sfctl.helps.container  # pylint: disable=unused-import
import sfctl.helps.property  # pylint: disable=unused-import
import sfctl.helps.app_type  # pylint: disable=unused-import
import sfctl.helps.chaos  # pylint: disable=unused-import
import sfctl.helps.infrastructure  # pylint: disable=unused-import
import sfctl.helps.node # pylint: disable=unused-import

EXCLUDED_PARAMS = ['self', 'raw', 'custom_headers', 'operation_config',
                   'content_version', 'kwargs', 'client']

class SFCommandHelp(CLIHelp):
    """Service Fabric CLI help loader"""

    def __init__(self, cli_ctx=None):
        header_msg = 'Service Fabric Command Line'

        super(SFCommandHelp, self).__init__(cli_ctx=cli_ctx, welcome_message=header_msg)


class SFCommandLoader(CLICommandsLoader):
    """Service Fabric CLI command loader, containing command mappings"""

    def __init__(self, *args, **kwargs):
        super(SFCommandLoader, self).__init__(
            *args,
            excluded_command_handler_args=EXCLUDED_PARAMS,
            **kwargs)

    def load_command_table(self, args):  # pylint: disable=too-many-statements
        """Load all Service Fabric commands"""

        # -----------------
        # Standard commands
        # -----------------

        client_func_path = 'azure.servicefabric#ServiceFabricClientAPIs.{}'

        with CommandGroup(self, 'rpm', client_func_path,
                          client_factory=client_create) as group:
            group.command('delete', 'delete_repair_task')
            group.command('list', 'get_repair_task_list')
            group.command('approve-force', 'force_approve_repair_task')

        with CommandGroup(self, 'sa-cluster', client_func_path,
                          client_factory=client_create) as group:
            group.command('config', 'get_cluster_configuration')
            group.command('upgrade-status',
                          'get_cluster_configuration_upgrade_status')

        with CommandGroup(self, 'cluster', client_func_path,
                          client_factory=client_create) as group:
            group.command('health', 'get_cluster_health')
            group.command('manifest', 'get_cluster_manifest')
            group.command(
                'code-versions',
                'get_provisioned_fabric_code_version_info_list'
            )
            group.command(
                'config-versions',
                'get_provisioned_fabric_config_version_info_list'
            )
            group.command('upgrade-status', 'get_cluster_upgrade_progress')
            group.command('recover-system', 'recover_system_partitions')
            group.command('operation-list', 'get_fault_operation_list')
            group.command('operation-cancel', 'cancel_operation')
            group.command('provision', 'provision_cluster')
            group.command('unprovision', 'unprovision_cluster')
            group.command('upgrade-rollback', 'rollback_cluster_upgrade')
            group.command('upgrade-resume', 'resume_cluster_upgrade')

        with CommandGroup(self, 'node', client_func_path,
                          client_factory=client_create) as group:
            group.command('list', 'get_node_info_list')
            group.command('info', 'get_node_info')
            group.command('health', 'get_node_health')
            group.command('load', 'get_node_load_info')
            group.command('disable', 'disable_node')
            group.command('enable', 'enable_node')
            group.command('remove-state', 'remove_node_state')
            group.command('restart', 'restart_node')
            group.command('transition', 'start_node_transition')
            group.command(
                'transition-status',
                'get_node_transition_progress'
            )
            group.command(
                'add-configuration-parameter-overrides',
                'add_configuration_parameter_overrides'
            )
            group.command(
                'get-configuration-overrides',
                'get_configuration_overrides'
            )
            group.command(
                'remove-configuration-overrides',
                'remove_configuration_overrides'
            )

        with CommandGroup(self, 'application', client_func_path,
                          client_factory=client_create) as group:
            group.command('type-list', 'get_application_type_info_list')
            group.command('type', 'get_application_type_info_list_by_name')
            group.command('unprovision', 'unprovision_application_type')
            group.command('delete', 'delete_application')
            group.command('list', 'get_application_info_list')
            group.command('info', 'get_application_info')
            group.command('health', 'get_application_health')
            group.command('upgrade-status', 'get_application_upgrade')
            group.command('upgrade-resume', 'resume_application_upgrade')
            group.command(
                'upgrade-rollback',
                'rollback_application_upgrade'
            )
            group.command(
                'deployed-list',
                'get_deployed_application_info_list'
            )
            group.command('deployed', 'get_deployed_application_info')
            group.command(
                'deployed-health',
                'get_deployed_application_health'
            )
            group.command('manifest', 'get_application_manifest')
            group.command('load', 'get_application_load_info')

        with CommandGroup(self, 'service', client_func_path,
                          client_factory=client_create) as group:
            group.command('type-list', 'get_service_type_info_list')
            group.command('manifest', 'get_service_manifest')
            group.command(
                'deployed-type-list',
                'get_deployed_service_type_info_list'
            )
            group.command(
                'deployed-type',
                'get_deployed_service_type_info_by_name'
            )
            group.command('list', 'get_service_info_list')
            group.command('info', 'get_service_info')
            group.command('app-name', 'get_application_name_info')
            group.command('delete', 'delete_service')
            group.command('description', 'get_service_description')
            group.command('health', 'get_service_health')
            group.command('resolve', 'resolve_service')
            group.command('recover', 'recover_service_partitions')
            group.command(
                'package-list',
                'get_deployed_service_package_info_list'
            )
            group.command(
                'package-info',
                'get_deployed_service_package_info_list_by_name'
            )
            group.command(
                'package-health',
                'get_deployed_service_package_health'
            )
            group.command(
                'code-package-list',
                'get_deployed_code_package_info_list'
            )
            group.command(
                'get-container-logs',
                'get_container_logs_deployed_on_node'
            )

        with CommandGroup(self, 'partition', client_func_path,
                          client_factory=client_create) as group:
            group.command('list', 'get_partition_info_list')
            group.command('info', 'get_partition_info')
            group.command('svc-name', 'get_service_name_info')
            group.command('health', 'get_partition_health')
            group.command('load', 'get_partition_load_information')
            group.command('load-reset', 'reset_partition_load')
            group.command('recover', 'recover_partition')
            group.command('recover-all', 'recover_all_partitions')
            group.command('data-loss', 'start_data_loss')
            group.command('data-loss-status', 'get_data_loss_progress')
            group.command('quorum-loss', 'start_quorum_loss')
            group.command('quorum-loss-status', 'get_quorum_loss_progress')
            group.command('restart', 'start_partition_restart')
            group.command(
                'restart-status',
                'get_partition_restart_progress'
            )
            group.command(
                'move-primary-replica',
                'move_primary_replica',
            )
            group.command(
                'move-secondary-replica',
                'move_secondary_replica',
            )
            group.command(
                'move-instance',
                'move_instance',
            )
            group.command(
                'get-loaded-partition-info-list',
                'get_loaded_partition_info_list',
            )

        with CommandGroup(self, 'replica', client_func_path,
                          client_factory=client_create) as group:
            group.command('list', 'get_replica_info_list')
            group.command('info', 'get_replica_info')
            group.command('health', 'get_replica_health')
            group.command(
                'deployed-list',
                'get_deployed_service_replica_info_list'
            )
            group.command(
                'deployed',
                'get_deployed_service_replica_detail_info'
            )
            group.command('restart', 'restart_replica')
            group.command('remove', 'remove_replica')

        with CommandGroup(self, 'compose', client_func_path,
                          client_factory=client_create) as group:
            group.command('status', 'get_compose_deployment_status')
            group.command('list', 'get_compose_deployment_status_list')
            group.command('remove', 'remove_compose_deployment')
            group.command('upgrade-status',
                          'get_compose_deployment_upgrade_progress')
            group.command('upgrade-rollback', 'start_rollback_compose_deployment_upgrade')

        with CommandGroup(self, 'chaos', client_func_path,
                          client_factory=client_create) as group:
            group.command('stop', 'stop_chaos')
            group.command('events', 'get_chaos_events')
            group.command('get', 'get_chaos')

        with CommandGroup(self, 'chaos schedule', client_func_path,
                          client_factory=client_create) as group:
            group.command('get', 'get_chaos_schedule')

        with CommandGroup(self, 'store', client_func_path,
                          client_factory=client_create) as group:
            group.command('stat', 'get_image_store_content')
            group.command('delete', 'delete_image_store_content')
            group.command('root-info', 'get_image_store_root_content')

        with CommandGroup(self, 'property', client_func_path,
                          client_factory=client_create) as group:
            group.command('list', 'get_property_info_list')
            group.command('get', 'get_property_info')
            group.command('delete', 'delete_property')

        with CommandGroup(self, 'events', client_func_path,
                          client_factory=client_create) as group:
            group.command('cluster-list', 'get_cluster_event_list')
            group.command('all-nodes-list', 'get_nodes_event_list')
            group.command('node-list', 'get_node_event_list')
            group.command('all-applications-list', 'get_applications_event_list')
            group.command('application-list', 'get_application_event_list')
            group.command('all-services-list', 'get_services_event_list')
            group.command('service-list', 'get_service_event_list')
            group.command('all-partitions-list', 'get_partitions_event_list')
            group.command('partition-list', 'get_partition_event_list')
            group.command('partition-all-replicas-list', 'get_partition_replicas_event_list')
            group.command('partition-replica-list', 'get_partition_replica_event_list')

        # ---------------
        # Custom commands
        # ---------------

        with CommandGroup(self, 'container', 'sfctl.custom_container#{}',
                          client_factory=client_create) as group:
            group.command('invoke-api', 'invoke_api')
            group.command('logs', 'logs')

        with CommandGroup(self, 'cluster', 'sfctl.custom_cluster_upgrade#{}',
                          client_factory=client_create) as group:
            group.command('upgrade', 'upgrade')
            group.command('upgrade-update', 'update_upgrade')

        with CommandGroup(self, 'sa-cluster', 'sfctl.custom_cluster_upgrade#{}',
                          client_factory=client_create) as group:
            group.command('config-upgrade', 'sa_configuration_upgrade')

        with CommandGroup(self, 'compose', 'sfctl.custom_compose#{}',
                          client_factory=client_create) as group:
            group.command('upgrade', 'upgrade')
            group.command('create', 'create')

        with CommandGroup(self, 'application', 'sfctl.custom_app#{}',
                          client_factory=client_create) as group:
            group.command('create', 'create')
            group.command('upgrade', 'upgrade')

        with CommandGroup(self, 'application', 'sfctl.custom_app#{}') as group:
            group.command('upload', 'upload')

        # Need an empty client for the select and upload operations
        with CommandGroup(self, 'cluster', 'sfctl.custom_cluster#{}') as group:
            group.command('select', 'select')
            group.command('show-connection', 'show_connection')

        with CommandGroup(self, 'chaos', 'sfctl.custom_chaos#{}',
                          client_factory=client_create) as group:
            group.command('start', 'start')

        with CommandGroup(self, 'chaos schedule', 'sfctl.custom_chaos_schedule#{}',
                          client_factory=client_create) as group:
            group.command('set', 'set_chaos_schedule')

        with CommandGroup(self, 'service', 'sfctl.custom_service#{}',
                          client_factory=client_create) as group:
            group.command('create', 'create')
            group.command('update', 'update')
            group.command('package-deploy', 'package_upload')

        with CommandGroup(self, 'is', 'sfctl.custom_is#{}',
                          client_factory=client_create) as group:
            group.command('command', 'is_command')
            group.command('query', 'is_query')

        with CommandGroup(self, 'property', 'sfctl.custom_property#{}',
                          client_factory=client_create) as group:
            group.command('put', 'naming_property_put')

        with CommandGroup(self, 'application', 'sfctl.custom_app_type#{}',
                          client_factory=client_create) as group:
            group.command('provision', 'provision_application_type')

        client_func_path_health = 'sfctl.custom_health#{}'

        with CommandGroup(self, 'application', client_func_path_health,
                          client_factory=client_create) as group:
            group.command('report-health', 'report_app_health')

        with CommandGroup(self, 'service', client_func_path_health,
                          client_factory=client_create) as group:
            group.command('report-health', 'report_svc_health')

        with CommandGroup(self, 'partition', client_func_path_health,
                          client_factory=client_create) as group:
            group.command('report-health', 'report_partition_health')

        with CommandGroup(self, 'replica', client_func_path_health,
                          client_factory=client_create) as group:
            group.command('report-health', 'report_replica_health')

        with CommandGroup(self, 'node', client_func_path_health,
                          client_factory=client_create) as group:
            group.command('report-health', 'report_node_health')

        with CommandGroup(self, 'cluster', client_func_path_health,
                          client_factory=client_create) as group:
            group.command('report-health', 'report_cluster_health')

        with CommandGroup(self, 'node', 'sfctl.custom_node#{}',
                          client_factory=client_create) as group:
            group.command('add-node-tags', 'add_node_tags')
            group.command('remove-node-tags', 'remove_node_tags')

        # ---------------
        # Settings
        # ---------------

        with CommandGroup(self, 'settings telemetry', 'sfctl.custom_settings#{}') as group:
            group.command('set-telemetry', 'set_telemetry')

        return OrderedDict(self.command_table)

    def load_arguments(self, command):
        """Load specialized arguments for commands"""
        from sfctl.params import custom_arguments

        custom_arguments(self, command)

        super(SFCommandLoader, self).load_arguments(command)
