# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Commands related to Service Fabric health entities and operations"""

from knack.util import CLIError

def parse_service_health_policy(policy):
    """Parse a health service policy from string"""

    if policy is None:
        return None

    uphp = policy.get('max_percent_unhealthy_partitions_per_service', 0)
    rhp = policy.get('max_percent_unhealthy_replicas_per_partition', 0)
    ushp = policy.get('max_percent_unhealthy_services', 0)
    return {"MaxPercentUnhealthyPartitionsPerService": uphp,
            "MaxpercentUnhealthyReplicasPerPartition": rhp,
            "MaxPercentUnhealthyServices": ushp}


def parse_service_health_policy_map(formatted_policy):
    """Parse a service health policy map from a string"""

    if formatted_policy is None:
        return None

    map_shp = []
    for st_desc in formatted_policy:
        st_name = st_desc.get('Key', None)

        if st_name is None:
            raise CLIError('Could not find service type name in service '
                           'health policy map')
        st_policy = st_desc.get('Value', None)
        if st_policy is None:
            raise CLIError('Could not find service type policy in service '
                           'health policy map')
        service_p = parse_service_health_policy(st_policy)
        std_list_item = {"Key": st_name, "Value": service_p}

        map_shp.append(std_list_item)
    return map_shp

def parse_app_health_map(formatted_map):
    """Parse application health map from string"""

    if not formatted_map:
        return None

    health_map = []
    for item in formatted_map:
        name = item.get('key', None)
        percent_unhealthy = item.get('value', None)
        if name is None:
            raise CLIError('Cannot find application type health policy map '
                           'name')
        if percent_unhealthy is None:
            raise CLIError('Cannot find application type health policy map '
                           'unhealthy percent')
        map_item = {"Key": name, "Value": percent_unhealthy}
        health_map.append(map_item)
    return health_map

def create_health_information(source_id, health_property, health_state, ttl,  #pylint: disable=too-many-arguments
                              description, sequence_number,
                              remove_when_expired):
    """Validates and creates a health information object"""
    # import distutils
    if health_state not in ['Invalid', 'Ok', 'Warning', 'Error', 'Unknown']:
        raise CLIError('Invalid health state specified')

    if isinstance(remove_when_expired, bool):
        rwe = remove_when_expired
    elif isinstance(remove_when_expired, str):
        rwe = remove_when_expired in ("True" , "true") #pylint: disable=simplifiable-if-statement

    return {"SourceId": source_id,
            "Property": health_property,
            "HealthState": health_state,
            "TimeToLiveInMilliSeconds": ttl,
            "Description": description,
            "SequenceNumber": sequence_number,
            "RemoveWhenExpired": rwe}


def report_cluster_health(client, source_id, health_property, health_state,  #pylint: disable=missing-docstring,too-many-arguments
                          ttl=None, description=None, sequence_number=None,
                          remove_when_expired=False, immediate=False,
                          timeout=60):
    health_info = create_health_information(source_id, health_property,
                                            health_state, ttl, description,
                                            sequence_number,
                                            remove_when_expired)

    client.report_cluster_health(health_info, immediate=immediate,
                                 timeout=timeout)


def report_app_health(client, application_id, #pylint: disable=missing-docstring,too-many-arguments
                      source_id, health_property, health_state, ttl=None,
                      description=None, sequence_number=None,
                      remove_when_expired=None, immediate=False, timeout=60):

    health_info = create_health_information(source_id, health_property,
                                            health_state, ttl, description,
                                            sequence_number,
                                            remove_when_expired)

    client.report_application_health(application_id, health_info,
                                     immediate=immediate, timeout=timeout)


def report_svc_health(client, service_id, source_id, health_property, #pylint: disable=missing-docstring,too-many-arguments
                      health_state, ttl=None, description=None,
                      sequence_number=None, remove_when_expired=None,
                      timeout=60, immediate=False):
    health_info = create_health_information(source_id, health_property,
                                            health_state, ttl, description,
                                            sequence_number,
                                            remove_when_expired)

    client.report_service_health(service_id, health_info, timeout=timeout,
                                 immediate=immediate)


def report_partition_health(client, partition_id, source_id, health_property, #pylint: disable=missing-docstring,too-many-arguments
                            health_state, ttl=None, description=None,
                            sequence_number=None, remove_when_expired=None,
                            immediate=False, timeout=60):

    health_info = create_health_information(source_id, health_property,
                                            health_state, ttl, description,
                                            sequence_number,
                                            remove_when_expired)

    client.report_partition_health(partition_id, health_info, timeout=timeout,
                                   immediate=immediate)

def report_replica_health(client, partition_id, replica_id, source_id, #pylint: disable=missing-docstring,too-many-arguments
                          health_state, health_property,
                          service_kind="Stateful", ttl=None, description=None,
                          sequence_number=None, remove_when_expired=None,
                          immediate=False, timeout=60):

    info = create_health_information(source_id, health_property, health_state,
                                     ttl, description, sequence_number,
                                     remove_when_expired)

    client.report_replica_health(partition_id, replica_id, info,
                                 service_kind=service_kind, timeout=timeout,
                                 immediate=immediate)


def report_node_health(client, node_name, source_id, health_property, #pylint: disable=missing-docstring,too-many-arguments
                       health_state, ttl=None, description=None,
                       sequence_number=None, remove_when_expired=None,
                       immediate=False, timeout=60):

    info = create_health_information(source_id, health_property, health_state,
                                     ttl, description, sequence_number,
                                     remove_when_expired)
    client.report_node_health(node_name, info, immediate=immediate, timeout=timeout)
