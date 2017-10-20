# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Custom parameter handling for commands"""
import json
from knack.arguments import ArgumentsContext

def json_encoded(arg_str):
    """Convert from argument JSON string to complex object"""

    return json.loads(arg_str)

def custom_arguments(self, _): #pylint: disable=too-many-statements
    """Load specialized arguments for commands"""

    # Global argument
    with ArgumentsContext(self, '') as arg_context:
        arg_context.argument('timeout', type=int, default=60,
                             options_list=('-t', '--timeout'),
                             help='Server timeout in seconds')

    with ArgumentsContext(self, 'application create') as arg_context:
        arg_context.argument('parameters', type=json_encoded)
        arg_context.argument('metrics', type=json_encoded)
        arg_context.argument('min_node_count', type=int)
        arg_context.argument('max_node_count', type=int)

    with ArgumentsContext(self, 'application list') as arg_context:
        arg_context.argument('application_definition_kind_filter', type=int)

    with ArgumentsContext(self, 'application upgrade') as arg_context:
        arg_context.argument('parameters', type=json_encoded)
        arg_context.argument('default_service_health_policy',
                             type=json_encoded)
        arg_context.argument('service_health_policy', type=json_encoded)
        arg_context.argument('replica_set_check_timeout', type=int)
        arg_context.argument('max_unhealthy_apps', type=int)

    with ArgumentsContext(self, 'service create') as arg_context:
        arg_context.argument('instance_count', type=int)
        arg_context.argument('target_replica_set_size', type=int)
        arg_context.argument('min_replica_set_size', type=int)
        arg_context.argument('replica_restart_wait', type=int)
        arg_context.argument('quorum_loss_wait', type=int)
        arg_context.argument('stand_by_replica_keep', type=int)
        arg_context.argument('load_metrics', type=json_encoded)
        arg_context.argument('placement_policy_list', type=json_encoded)

    with ArgumentsContext(self, 'service update') as arg_context:
        arg_context.argument('instance_count', type=int)
        arg_context.argument('target_replica_set_size', type=int)
        arg_context.argument('min_replica_set_size', type=int)
        arg_context.argument('load_metrics', type=json_encoded)

    with ArgumentsContext(self, 'chaos start') as arg_context:
        arg_context.argument('app_type_health_policy_map', type=json_encoded)
        arg_context.argument('max_cluster_stabilization', type=int)
        arg_context.argument('max_concurrent_faults', type=int)
        arg_context.argument('wait_time_between_faults', type=int)
        arg_context.argument('wait_time_between_iterations', type=int)
        arg_context.argument('max_percent_unhealthy_nodes', type=int)
        arg_context.argument('max_percent_unhealthy_apps', type=int)

    with ArgumentsContext(self, 'cluster health') as arg_context:
        arg_context.argument('nodes_health_state_filter', type=int)
        arg_context.argument('applications_health_state_filter', type=int)
        arg_context.argument('events_health_state_filter', type=int)

    with ArgumentsContext(self, 'node health') as arg_context:
        arg_context.argument('events_health_state_filter', type=int)

    with ArgumentsContext(self, 'application health') as arg_context:
        arg_context.argument('events_health_state_filter', type=int)
        arg_context.argument('deployed_applications_health_state_filter',
                             type=int)
        arg_context.argument('services_health_state_filter', type=int)

    with ArgumentsContext(self, 'application deployed-health') as arg_context:
        arg_context.argument('events_health_state_filter', type=int)
        arg_context.argument('deployed_service_packages_health_state_filter',
                             type=int)

    with ArgumentsContext(self, 'service health') as arg_context:
        arg_context.argument('events_health_state_filter', type=int)
        arg_context.argument('partitions_health_state_filter', type=int)

    with ArgumentsContext(self, 'service resolve') as arg_context:
        arg_context.argument('partition_key_type', type=int)

    with ArgumentsContext(self, 'partition health') as arg_context:
        arg_context.argument('events_health_state_filter', type=int)
        arg_context.argument('replicas_health_state_filter', type=int)

    with ArgumentsContext(self, 'replica health') as arg_context:
        arg_context.argument('events_health_state_filter', type=int)

    with ArgumentsContext(self, 'service package-health') as arg_context:
        arg_context.argument('events_health_state_filter', type=int)

    with ArgumentsContext(self, 'partition quorum-loss') as arg_context:
        arg_context.argument('quorum_loss_duration', type=int)

    with ArgumentsContext(self, 'node transition') as arg_context:
        arg_context.argument('stop_duration_in_seconds', type=int)

    with ArgumentsContext(self, 'cluster operation-list') as arg_context:
        arg_context.argument('type_filter', type=int)
        arg_context.argument('state_filter', type=int)

    with ArgumentsContext(self, 'application type-list') as arg_context:
        arg_context.argument('max_results', type=int)
        arg_context.argument('application_type_definition_kind_filter',
                             type=int)

    with ArgumentsContext(self, 'application type') as arg_context:
        arg_context.argument('max_results', type=int)

    with ArgumentsContext(self, 'compose list') as arg_context:
        arg_context.argument('max_results', type=int)

    with ArgumentsContext(self, 'cluster upgrade') as arg_context:
        arg_context.argument('replica_set_check_timeout', type=int)
        arg_context.argument('unhealthy_nodes', type=int)
        arg_context.argument('unhealthy_applications', type=int)
        arg_context.argument('app_type_health_map', type=json_encoded)
        arg_context.argument('delta_unhealthy_nodes', type=int)
        arg_context.argument('upgrade_domain_delta_unhealthy_nodes', type=int)
        arg_context.argument('app_health_map', type=json_encoded)

    with ArgumentsContext(self, 'sa-cluster config-upgrade') as arg_context:
        arg_context.argument('unhealthy_applications', type=int)
        arg_context.argument('unhealthy_nodes', type=int)
        arg_context.argument('delta_unhealthy_nodes', type=int)
        arg_context.argument('upgrade_domain_delta_unhealthy_nodes', type=int)

    with ArgumentsContext(self, 'cluster upgrade-update') as arg_context:
        arg_context.argument('replica_set_check_timeout', type=int)
        arg_context.argument('unhealthy_nodes', type=int)
        arg_context.argument('unhealthy_applications', type=int)
        arg_context.argument('app_type_health_map', type=json_encoded)
        arg_context.argument('delta_unhealthy_nodes', type=int)
        arg_context.argument('upgrade_domain_delta_unhealthy_nodes', type=int)
        arg_context.argument('app_health_map', type=json_encoded)

    with ArgumentsContext(self, 'rpm list') as arg_context:
        arg_context.argument('state_filter', type=int)

    with ArgumentsContext(self, 'compose upgrade') as arg_context:
        arg_context.argument('unhealthy_app', type=int)
        arg_context.argument('default_svc_type_health_map', type=json_encoded)
        arg_context.argument('svc_type_health_map', type=json_encoded)
