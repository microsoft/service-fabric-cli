

def parse_default_service_health_policy(policy):
    from azure.servicefabric.models.service_type_health_policy import ServiceTypeHealthPolicy

    if policy is None:
        return None

    uphp = policy.get("max_percent_unhealthy_partitions_per_service", 0)
    rhp = policy.get("max_percent_unhealthy_replicas_per_partition", 0)
    ushp = policy.get("max_percent_unhealthy_services", 0)
    return ServiceTypeHealthPolicy(uphp, rhp, ushp)


def parse_service_health_policy_map(formatted_policy):
    from azure.servicefabric.models.service_type_health_policy_map_item import ServiceTypeHealthPolicyMapItem

    if formatted_policy is None:
        return None

    map_shp = []
    for st_desc in formatted_policy:
        st_name = st_desc.get("Key", None)
        if st_name is None:
            raise CLIError("Could not find service type name in service health policy map")
        st_policy = st_desc.get("Value", None)
        if st_policy is None:
            raise CLIError("Could not find service type policy in service health policy map")
        p = parse_default_service_health_policy(st_policy)
        std_list_item = ServiceTypeHealthPolicyMapItem(st_name, p)

        map_shp.append(std_list_item)
    return map_shp

def parse_app_health_map(formatted_map):
    from azure.servicefabric.models.application_type_health_policy_map_item import ApplicationTypeHealthPolicyMapItem

    if not formatted_map:
        return None

    health_map = []
    for m in formatted_map:
        name = m.get("key", None)
        percent_unhealthy = m.get("value", None)
        if name is None:
            raise CLIError("Cannot find application type health policy map name")
        if percent_unhealthy is None:
            raise CLIError("Cannot find application type health policy map unhealthy percent")
        r = ApplicationTypeHealthPolicyMapItem(name, percent_unhealthy)
        health_map.append(r)
    return health_map

