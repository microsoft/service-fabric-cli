"""Commands for managing the health of service fabric entities"""
from knack.util import CLIError

def parse_def_service_health_policy(policy):
    """Parse default service health policy from string"""

    from azure.servicefabric.models.service_type_health_policy import (
        ServiceTypeHealthPolicy
    )

    if policy is None:
        return None

    uphp = policy.get("max_percent_unhealthy_partitions_per_service", 0)
    rhp = policy.get("max_percent_unhealthy_replicas_per_partition", 0)
    ushp = policy.get("max_percent_unhealthy_services", 0)
    return ServiceTypeHealthPolicy(uphp, rhp, ushp)


def parse_service_health_policy_map(formatted_policy):
    """Parse a service health policy mapping from a string"""
    from azure.servicefabric.models.service_type_health_policy_map_item import ServiceTypeHealthPolicyMapItem  # pylint: disable=line-too-long

    if formatted_policy is None:
        return None

    map_shp = []
    for st_desc in formatted_policy:
        st_name = st_desc.get("Key", None)
        if st_name is None:
            raise CLIError("Could not find service type name in service health"
                           " policy map")
        st_policy = st_desc.get("Value", None)
        if st_policy is None:
            raise CLIError("Could not find service type policy in service "
                           "health policy map")
        poli = parse_def_service_health_policy(st_policy)
        std_list_item = ServiceTypeHealthPolicyMapItem(st_name, poli)

        map_shp.append(std_list_item)
    return map_shp

def parse_app_health_map(formatted_map):
    """Parse an application health policy mapping from a string"""
    from azure.servicefabric.models.application_type_health_policy_map_item import ApplicationTypeHealthPolicyMapItem # pylint: disable=line-too-long

    if not formatted_map:
        return None

    health_map = []
    for i in formatted_map:
        name = i.get("key", None)
        percent_unhealthy = i.get("value", None)
        if name is None:
            raise CLIError("Cannot find application type health policy map "
                           "name")
        if percent_unhealthy is None:
            raise CLIError("Cannot find application type health policy map "
                           "unhealthy percent")
        map_item = ApplicationTypeHealthPolicyMapItem(name, percent_unhealthy)
        health_map.append(map_item)
    return health_map
