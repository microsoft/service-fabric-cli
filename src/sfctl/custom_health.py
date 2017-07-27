# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Commands related to Service Fabric health entities and operations"""

from knack.util import CLIError

def parse_service_health_policy(policy):
    """Parse a health service policy from string"""
    from azure.servicefabric.models.service_type_health_policy import (
        ServiceTypeHealthPolicy
    )

    if policy is None:
        return None

    uphp = policy.get('max_percent_unhealthy_partitions_per_service', 0)
    rhp = policy.get('max_percent_unhealthy_replicas_per_partition', 0)
    ushp = policy.get('max_percent_unhealthy_services', 0)
    return ServiceTypeHealthPolicy(uphp, rhp, ushp)

def parse_service_health_policy_map(formatted_policy):
    """Parse a service health policy map from a string"""

    from azure.servicefabric.models.service_type_health_policy_map_item import ServiceTypeHealthPolicyMapItem  #pylint: disable=line-too-long

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
        std_list_item = ServiceTypeHealthPolicyMapItem(st_name, service_p)

        map_shp.append(std_list_item)
    return map_shp

def parse_app_health_map(formatted_map):
    """Parse application health map from string"""

    from azure.servicefabric.models.application_type_health_policy_map_item import ApplicationTypeHealthPolicyMapItem #pylint: disable=line-too-long

    if not formatted_map:
        return None

    health_map = []
    for m in formatted_map:
        name = m.get('key', None)
        percent_unhealthy = m.get('value', None)
        if name is None:
            raise CLIError('Cannot find application type health policy map '
                           'name')
        if percent_unhealthy is None:
            raise CLIError('Cannot find application type health policy map '
                           'unhealthy percent')
        map_item = ApplicationTypeHealthPolicyMapItem(name, percent_unhealthy)
        health_map.append(map_item)
    return health_map

def report_app_health(client, application_id,
                      source_id, health_property, health_state, ttl=None,
                      description=None, sequence_number=None,
                      remove_when_expired=None, timeout=60):
    """
    Sends a health report on the Service Fabric application.
    Reports health state of the specified Service Fabric application. The
    report must contain the information about the source of the health report
    and property on which it is reported. The report is sent to a Service
    Fabric gateway Application, which forwards to the health store. The report
    may be accepted by the gateway, but rejected by the health store after
    extra validation. For example, the health store may reject the report
    because of an invalid parameter, like a stale sequence number. To see
    whether the report was applied in the health store, check that the report
    appears in the events section.
    :param str application_id: The identity of the application. This is
    typically the full name of the application without the 'fabric:' URI
    scheme.
    :param str source_id: The source name which identifies the
    client/watchdog/system component which generated the health information.
    :param str health_property: The property of the health information. An
    entity can have health reports for different properties. The property is a
    string and not a fixed enumeration to allow the reporter flexibility to
    categorize the state condition that triggers the report. For example, a
    reporter with SourceId "LocalWatchdog" can monitor the state of the
    available disk on a node, so it can report "AvailableDisk" property on
    that node. The same reporter can monitor the node connectivity, so it can
    report a property "Connectivity" on the same node. In the health store,
    these reports are treated as separate health events for the specified node.
    Together with the SourceId, the property uniquely identifies the health
    information.
    :param str health_state: Possible values include: 'Invalid', 'Ok',
    'Warning', 'Error', 'Unknown'
    :param str ttl: The duration, in milliseconds, for which this health report
    is valid. When clients report periodically, they should send reports with
    higher frequency than time to live. If not specified, time to live defaults
    to infinite value.
    :param str description: The description of the health information. It
    represents free text used to add human readable information about the
    report. The maximum string length for the description is 4096 characters.
    If the provided string is longer, it will be automatically truncated.
    When truncated, the last characters of the description contain a marker
    "[Truncated]", and total string size is 4096 characters. The presence of
    the marker indicates to users that truncation occurred. Note that when
    truncated, the description has less than 4096 characters from the original
    string.
    :param str sequence_number: The sequence number for this health report as a
    numeric string. The report sequence number is used by the health store to
    detect stale reports. If not specified, a sequence number is auto-generated
    by the health client when a report is added.
    :param bool remove_when_expired: Value that indicates whether the report is
    removed from health store when it expires. If set to true, the report is
    removed from the health store after it expires. If set to false, the report
    is treated as an error when expired. The value of this property is false by
    default. When clients report periodically, they should set this value to
    false (default). This way, is the reporter has issues (eg. deadlock) and
    can't report, the entity is evaluated at error when the health report
    expires. This flags the entity as being in Error health state.
    """

    from azure.servicefabric.models.health_information import HealthInformation

    info = HealthInformation(source_id, health_property, health_state, ttl,
                             description, sequence_number, remove_when_expired)

    client.report_application_health(application_id, info, timeout)


def report_svc_health(client, service_id, source_id, health_property,
                      health_state, ttl=None, description=None,
                      sequence_number=None, remove_when_expired=None,
                      timeout=60):
    """
    Sends a health report on the Service Fabric service.
    Reports health state of the specified Service Fabric service. The
    report must contain the information about the source of the health
    report and property on which it is reported. The report is sent to a
    Service Fabric gateway Service, which forwards to the health store.
    The report may be accepted by the gateway, but rejected by the health
    store after extra validation. For example, the health store may reject
    the report because of an invalid parameter, like a stale sequence number.
    To see whether the report was applied in the health store, check that the
    report appears in the health events of the service.
    :param str service_id: The identity of the service. This is typically the
    full name of the service without the 'fabric:' URI scheme.
    :param str source_id: The source name which identifies the
    client/watchdog/system component which generated the health information.
    :param str health_property: The property of the health information. An
    entity can have health reports for different properties. The property is a
    string and not a fixed enumeration to allow the reporter flexibility to
    categorize the state condition that triggers the report. For example, a
    reporter with SourceId "LocalWatchdog" can monitor the state of the
    available disk on a node, so it can report "AvailableDisk" property on
    that node. The same reporter can monitor the node connectivity, so it can
    report a property "Connectivity" on the same node. In the health store,
    these reports are treated as separate health events for the specified node.
    Together with the SourceId, the property uniquely identifies the health
    information.
    :param str health_state: Possible values include: 'Invalid', 'Ok',
    'Warning', 'Error', 'Unknown'
    :param str ttl: The duration, in milliseconds, for which this health report
    is valid. When clients report periodically, they should send reports with
    higher frequency than time to live. If not specified, time to live defaults
    to infinite value.
    :param str description: The description of the health information. It
    represents free text used to add human readable information about the
    report. The maximum string length for the description is 4096 characters.
    If the provided string is longer, it will be automatically truncated.
    When truncated, the last characters of the description contain a marker
    "[Truncated]", and total string size is 4096 characters. The presence of
    the marker indicates to users that truncation occurred. Note that when
    truncated, the description has less than 4096 characters from the original
    string.
    :param str sequence_number: The sequence number for this health report as a
    numeric string. The report sequence number is used by the health store to
    detect stale reports. If not specified, a sequence number is auto-generated
    by the health client when a report is added.
    :param bool remove_when_expired: Value that indicates whether the report is
    removed from health store when it expires. If set to true, the report is
    removed from the health store after it expires. If set to false, the report
    is treated as an error when expired. The value of this property is false by
    default. When clients report periodically, they should set this value to
    false (default). This way, is the reporter has issues (eg. deadlock) and
    can't report, the entity is evaluated at error when the health report
    expires. This flags the entity as being in Error health state.
    """

    from azure.servicefabric.models.health_information import HealthInformation

    info = HealthInformation(source_id, health_property, health_state, ttl,
                             description, sequence_number, remove_when_expired)

    client.report_service_health(service_id, info, timeout)


def report_partition_health(client, partition_id, source_id, health_property,
                            health_state, ttl=None, description=None,
                            sequence_number=None, remove_when_expired=None,
                            timeout=60):
    """
    Sends a health report on the Service Fabric partition.
    Reports health state of the specified Service Fabric partition. The
    report must contain the information about the source of the health
    report and property on which it is reported. The report is sent to a
    Service Fabric gateway Partition, which forwards to the health store.
    The report may be accepted by the gateway, but rejected by the health
    store after extra validation. For example, the health store may reject
    the report because of an invalid parameter, like a stale sequence number.
    To see whether the report was applied in the health store, check that the
    report appears in the events section.
    :param str partition_id: The identity of the partition.
    :param str source_id: The source name which identifies the
    client/watchdog/system component which generated the health information.
    :param str health_property: The property of the health information. An
    entity can have health reports for different properties. The property is a
    string and not a fixed enumeration to allow the reporter flexibility to
    categorize the state condition that triggers the report. For example, a
    reporter with SourceId "LocalWatchdog" can monitor the state of the
    available disk on a node, so it can report "AvailableDisk" property on
    that node. The same reporter can monitor the node connectivity, so it can
    report a property "Connectivity" on the same node. In the health store,
    these reports are treated as separate health events for the specified node.
    Together with the SourceId, the property uniquely identifies the health
    information.
    :param str health_state: Possible values include: 'Invalid', 'Ok',
    'Warning', 'Error', 'Unknown'
    :param str ttl: The duration, in milliseconds, for which this health report
    is valid. When clients report periodically, they should send reports with
    higher frequency than time to live. If not specified, time to live defaults
    to infinite value.
    :param str description: The description of the health information. It
    represents free text used to add human readable information about the
    report. The maximum string length for the description is 4096 characters.
    If the provided string is longer, it will be automatically truncated.
    When truncated, the last characters of the description contain a marker
    "[Truncated]", and total string size is 4096 characters. The presence of
    the marker indicates to users that truncation occurred. Note that when
    truncated, the description has less than 4096 characters from the original
    string.
    :param str sequence_number: The sequence number for this health report as a
    numeric string. The report sequence number is used by the health store to
    detect stale reports. If not specified, a sequence number is auto-generated
    by the health client when a report is added.
    :param bool remove_when_expired: Value that indicates whether the report is
    removed from health store when it expires. If set to true, the report is
    removed from the health store after it expires. If set to false, the report
    is treated as an error when expired. The value of this property is false by
    default. When clients report periodically, they should set this value to
    false (default). This way, is the reporter has issues (eg. deadlock) and
    can't report, the entity is evaluated at error when the health report
    expires. This flags the entity as being in Error health state.
    """

    from azure.servicefabric.models.health_information import HealthInformation

    info = HealthInformation(source_id, health_property, health_state, ttl,
                             description, sequence_number, remove_when_expired)
    client.report_partition_health(partition_id, info, timeout)


def report_replica_health(client, partition_id, replica_id, source_id,
                          health_state, health_property,
                          service_kind="Stateful", ttl=None, description=None,
                          sequence_number=None, remove_when_expired=None,
                          timeout=60):
    """
    Sends a health report on the Service Fabric replica.
    Reports health state of the specified Service Fabric replica. The
    report must contain the information about the source of the health
    report and property on which it is reported. The report is sent to a
    Service Fabric gateway Replica, which forwards to the health store. The
    report may be accepted by the gateway, but rejected by the health store
    after extra validation. For example, the health store may reject the
    report because of an invalid parameter, like a stale sequence number.
    To see whether the report was applied in the health store, check that
    the report appears in the events section.
    :param str partition_id: The identity of the partition.
    :param str replica_id: The identifier of the replica.
    :param str service_kind: The kind of service replica (Stateless or
    Stateful) for which the health is being reported. Following are the
    possible values: `Stateless`, `Stateful`.
     :param str source_id: The source name which identifies the
    client/watchdog/system component which generated the health information.
    :param str health_property: The property of the health information. An
    entity can have health reports for different properties. The property is a
    string and not a fixed enumeration to allow the reporter flexibility to
    categorize the state condition that triggers the report. For example, a
    reporter with SourceId "LocalWatchdog" can monitor the state of the
    available disk on a node, so it can report "AvailableDisk" property on
    that node. The same reporter can monitor the node connectivity, so it can
    report a property "Connectivity" on the same node. In the health store,
    these reports are treated as separate health events for the specified node.
    Together with the SourceId, the property uniquely identifies the health
    information.
    :param str health_state: Possible values include: 'Invalid', 'Ok',
    'Warning', 'Error', 'Unknown'
    :param str ttl: The duration, in milliseconds, for which this health report
    is valid. When clients report periodically, they should send reports with
    higher frequency than time to live. If not specified, time to live defaults
    to infinite value.
    :param str description: The description of the health information. It
    represents free text used to add human readable information about the
    report. The maximum string length for the description is 4096 characters.
    If the provided string is longer, it will be automatically truncated.
    When truncated, the last characters of the description contain a marker
    "[Truncated]", and total string size is 4096 characters. The presence of
    the marker indicates to users that truncation occurred. Note that when
    truncated, the description has less than 4096 characters from the original
    string.
    :param str sequence_number: The sequence number for this health report as a
    numeric string. The report sequence number is used by the health store to
    detect stale reports. If not specified, a sequence number is auto-generated
    by the health client when a report is added.
    :param bool remove_when_expired: Value that indicates whether the report is
    removed from health store when it expires. If set to true, the report is
    removed from the health store after it expires. If set to false, the report
    is treated as an error when expired. The value of this property is false by
    default. When clients report periodically, they should set this value to
    false (default). This way, is the reporter has issues (eg. deadlock) and
    can't report, the entity is evaluated at error when the health report
    expires. This flags the entity as being in Error health state.
    """

    from azure.servicefabric.models.health_information import HealthInformation

    info = HealthInformation(source_id, health_property, health_state, ttl,
                             description, sequence_number, remove_when_expired)

    client.report_replica_health(partition_id, replica_id, info,
                                 service_kind, timeout)


def report_node_health(client, node_name, source_id, health_property,
                       health_state, ttl=None, description=None,
                       sequence_number=None, remove_when_expired=None,
                       timeout=60):
    """
    Sends a health report on the Service Fabric node.
    Reports health state of the specified Service Fabric node. The report
    must contain the information about the source of the health report
    and property on which it is reported. The report is sent to a Service
    Fabric gateway node, which forwards to the health store. The report may be
    accepted by the gateway, but rejected by the health store after extra
    validation. For example, the health store may reject the report because of
    an invalid parameter, like a stale sequence number. To see whether the
    report was applied in the health store, check that the report appears in
    the events section.
    :param str node_name: The name of the node.
    :param str source_id: The source name which identifies the
    client/watchdog/system component which generated the health information.
    :param str health_property: The property of the health information. An
    entity can have health reports for different properties. The property is a
    string and not a fixed enumeration to allow the reporter flexibility to
    categorize the state condition that triggers the report. For example, a
    reporter with SourceId "LocalWatchdog" can monitor the state of the
    available disk on a node, so it can report "AvailableDisk" property on
    that node. The same reporter can monitor the node connectivity, so it can
    report a property "Connectivity" on the same node. In the health store,
    these reports are treated as separate health events for the specified node.
    Together with the SourceId, the property uniquely identifies the health
    information.
    :param str health_state: Possible values include: 'Invalid', 'Ok',
    'Warning', 'Error', 'Unknown'
    :param str ttl: The duration, in milliseconds, for which this health report
    is valid. When clients report periodically, they should send reports with
    higher frequency than time to live. If not specified, time to live defaults
    to infinite value.
    :param str description: The description of the health information. It
    represents free text used to add human readable information about the
    report. The maximum string length for the description is 4096 characters.
    If the provided string is longer, it will be automatically truncated.
    When truncated, the last characters of the description contain a marker
    "[Truncated]", and total string size is 4096 characters. The presence of
    the marker indicates to users that truncation occurred. Note that when
    truncated, the description has less than 4096 characters from the original
    string.
    :param str sequence_number: The sequence number for this health report as a
    numeric string. The report sequence number is used by the health store to
    detect stale reports. If not specified, a sequence number is auto-generated
    by the health client when a report is added.
    :param bool remove_when_expired: Value that indicates whether the report is
    removed from health store when it expires. If set to true, the report is
    removed from the health store after it expires. If set to false, the report
    is treated as an error when expired. The value of this property is false by
    default. When clients report periodically, they should set this value to
    false (default). This way, is the reporter has issues (eg. deadlock) and
    can't report, the entity is evaluated at error when the health report
    expires. This flags the entity as being in Error health state.
    """

    from azure.servicefabric.models.health_information import HealthInformation

    info = HealthInformation(source_id, health_property, health_state, ttl,
                             description, sequence_number, remove_when_expired)

    client.report_node_health(node_name, info, timeout)
