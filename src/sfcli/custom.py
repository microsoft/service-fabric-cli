"""Custom commands.

Custom commands are useful when the Service Fabric client requires complex
objects as arguments, or does not have existing matching functions."""

# pylint: disable=too-many-lines

import os
import sys
import requests

from urllib.parse import urlparse, urlencode, urlunparse
from knack.util import CLIError



def sf_report_app_health(client, application_id,
                         source_id, health_property,
                         health_state, ttl=None, description=None,
                         sequence_number=None, remove_when_expired=None,
                         timeout=60):
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


def sf_report_svc_health(client, service_id,
                         source_id, health_property, health_state,
                         ttl=None, description=None, sequence_number=None,
                         remove_when_expired=None, timeout=60):
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

    # TODO Move common HealthInformation params to _params

    from azure.servicefabric.models.health_information import HealthInformation

    info = HealthInformation(source_id, health_property, health_state, ttl,
                             description, sequence_number, remove_when_expired)

    client.report_service_health(service_id, info, timeout)


def sf_report_partition_health(
        client, partition_id, source_id, health_property, health_state, ttl=None,
        description=None, sequence_number=None, remove_when_expired=None,
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

    # TODO Move common HealthInformation params to _params

    from azure.servicefabric.models.health_information import HealthInformation

    info = HealthInformation(source_id, health_property, health_state, ttl,
                             description, sequence_number, remove_when_expired)
    client.report_partition_health(partition_id, info, timeout)


def sf_report_replica_health(
        client, partition_id, replica_id, source_id, health_state, health_property,
        service_kind="Stateful", ttl=None, description=None,
        sequence_number=None, remove_when_expired=None, timeout=60):
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

    # TODO Move common HealthInformation params to _params

    from azure.servicefabric.models.health_information import HealthInformation

    info = HealthInformation(source_id, health_property, health_state, ttl,
                             description, sequence_number, remove_when_expired)

    client.report_replica_health(partition_id, replica_id, info,
                                 service_kind, timeout)


def sf_report_node_health(client, node_name,
                          source_id, health_property, health_state,
                          ttl=None, description=None, sequence_number=None,
                          remove_when_expired=None, timeout=60):
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

    # TODO Move common HealthInformation params to _params

    from azure.servicefabric.models.health_information import HealthInformation

    info = HealthInformation(source_id, health_property, health_state, ttl,
                             description, sequence_number, remove_when_expired)

    client.report_node_health(node_name, info, timeout)
