# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

def get_cluster_event_list(client, start_time_utc, end_time_utc, events_types_filter=None, exclude_analysis_events=None, skip_correlation_lookup=None, timeout=60):
    """Gets all CLuster-related events.

    The response is list of ClusterEvent objects.

    :param start_time_utc: The start time of a lookup query in ISO UTC yyyy-MM-ddTHH:mm:ssZ.
    :paramtype start_time_utc: str
    :param end_time_utc: The end time of a lookup query in ISO UTC yyyy-MM-ddTHH:mm:ssZ.
    :paramtype end_time_utc: str
    :param timeout: The server timeout for performing the operation in seconds. This timeout
        specifies the time duration that the client is willing to wait for the requested operation to
        complete. The default value for this parameter is 60 seconds. Default value is 60.
    :paramtype timeout: long
    :param events_types_filter: This is a comma separated string specifying the types of
        FabricEvents that should only be included in the response. Default value is None.
    :paramtype events_types_filter: str
    :param exclude_analysis_events: This param disables the retrieval of AnalysisEvents if true
        is passed. Default value is None.
    :paramtype exclude_analysis_events: bool
    :param skip_correlation_lookup: This param disables the search of CorrelatedEvents
        information if true is passed. otherwise the CorrelationEvents get processed and
        HasCorrelatedEvents field in every FabricEvent gets populated. Default value is None.
        """
    return client.get_cluster_event_list(start_time_utc=start_time_utc, end_time_utc=end_time_utc, events_types_filter=events_types_filter, 
                                              exclude_analysis_events=exclude_analysis_events, 
                                              skip_correlation_lookup=skip_correlation_lookup, timeout=timeout)

def get_nodes_event_list(client, start_time_utc, end_time_utc, events_types_filter=None, exclude_analysis_events=None, skip_correlation_lookup=None, timeout=60):
    """Gets all Nodes-related events.

    The response is list of NodeEvent objects.

    :param start_time_utc: The start time of a lookup query in ISO UTC yyyy-MM-ddTHH:mm:ssZ.
    :paramtype start_time_utc: str
    :param end_time_utc: The end time of a lookup query in ISO UTC yyyy-MM-ddTHH:mm:ssZ.
    :paramtype end_time_utc: str
    :param timeout: The server timeout for performing the operation in seconds. This timeout
        specifies the time duration that the client is willing to wait for the requested operation to
        complete. The default value for this parameter is 60 seconds. Default value is 60.
    :paramtype timeout: long
    :param events_types_filter: This is a comma separated string specifying the types of
        FabricEvents that should only be included in the response. Default value is None.
    :paramtype events_types_filter: str
    :param exclude_analysis_events: This param disables the retrieval of AnalysisEvents if true
        is passed. Default value is None.
    :paramtype exclude_analysis_events: bool
    :param skip_correlation_lookup: This param disables the search of CorrelatedEvents
        information if true is passed. otherwise the CorrelationEvents get processed and
        HasCorrelatedEvents field in every FabricEvent gets populated. Default value is None.
        """
    return client.get_nodes_event_list(start_time_utc=start_time_utc, end_time_utc=end_time_utc, events_types_filter=events_types_filter, 
                                              exclude_analysis_events=exclude_analysis_events, 
                                              skip_correlation_lookup=skip_correlation_lookup, timeout=timeout)

def get_node_event_list(client, node_name, start_time_utc, end_time_utc, events_types_filter=None, exclude_analysis_events=None, skip_correlation_lookup=None, timeout=60):
    """Gets all Node-related events for a specific node.

    The response is list of NodeEvent objects.

    :param node_name: The name of the node.
    :type node_name: str
    :param start_time_utc: The start time of a lookup query in ISO UTC yyyy-MM-ddTHH:mm:ssZ.
    :paramtype start_time_utc: str
    :param end_time_utc: The end time of a lookup query in ISO UTC yyyy-MM-ddTHH:mm:ssZ.
    :paramtype end_time_utc: str
    :param timeout: The server timeout for performing the operation in seconds. This timeout
        specifies the time duration that the client is willing to wait for the requested operation to
        complete. The default value for this parameter is 60 seconds. Default value is 60.
    :paramtype timeout: long
    :param events_types_filter: This is a comma separated string specifying the types of
        FabricEvents that should only be included in the response. Default value is None.
    :paramtype events_types_filter: str
    :param exclude_analysis_events: This param disables the retrieval of AnalysisEvents if true
        is passed. Default value is None.
    :paramtype exclude_analysis_events: bool
    :param skip_correlation_lookup: This param disables the search of CorrelatedEvents
        information if true is passed. otherwise the CorrelationEvents get processed and
        HasCorrelatedEvents field in every FabricEvent gets populated. Default value is None.
        """
    return client.get_node_event_list(node_name, start_time_utc=start_time_utc, end_time_utc=end_time_utc, events_types_filter=events_types_filter, 
                                              exclude_analysis_events=exclude_analysis_events, 
                                              skip_correlation_lookup=skip_correlation_lookup, timeout=timeout)

def get_applications_event_list(client, start_time_utc, end_time_utc, events_types_filter=None, exclude_analysis_events=None, skip_correlation_lookup=None, timeout=60):
    """Gets all Applications-related events.

    The response is list of ApplicationEvent objects.

    :param start_time_utc: The start time of a lookup query in ISO UTC yyyy-MM-ddTHH:mm:ssZ.
    :paramtype start_time_utc: str
    :param end_time_utc: The end time of a lookup query in ISO UTC yyyy-MM-ddTHH:mm:ssZ.
    :paramtype end_time_utc: str
    :param timeout: The server timeout for performing the operation in seconds. This timeout
        specifies the time duration that the client is willing to wait for the requested operation to
        complete. The default value for this parameter is 60 seconds. Default value is 60.
    :paramtype timeout: long
    :param events_types_filter: This is a comma separated string specifying the types of
        FabricEvents that should only be included in the response. Default value is None.
    :paramtype events_types_filter: str
    :param exclude_analysis_events: This param disables the retrieval of AnalysisEvents if true
        is passed. Default value is None.
    :paramtype exclude_analysis_events: bool
    :param skip_correlation_lookup: This param disables the search of CorrelatedEvents
        information if true is passed. otherwise the CorrelationEvents get processed and
        HasCorrelatedEvents field in every FabricEvent gets populated. Default value is None.
        """
    return client.get_applications_event_list(start_time_utc=start_time_utc, end_time_utc=end_time_utc, events_types_filter=events_types_filter, 
                                              exclude_analysis_events=exclude_analysis_events, 
                                              skip_correlation_lookup=skip_correlation_lookup, timeout=timeout)

def get_application_event_list(client, application_id, start_time_utc, end_time_utc, events_types_filter=None, exclude_analysis_events=None, skip_correlation_lookup=None, timeout=60):
    """Gets all Applications-related events for a specific application.

    The response is list of ApplicationEvent objects.

    :param application_id: The identity of the application. This is typically the full name of the
        application without the 'fabric:' URI scheme.
        Starting from version 6.0, hierarchical names are delimited with the "~" character.
        For example, if the application name is "fabric:/myapp/app1", the application identity would
        be "myapp~app1" in 6.0+ and "myapp/app1" in previous versions.
    :type application_id: str
    :param start_time_utc: The start time of a lookup query in ISO UTC yyyy-MM-ddTHH:mm:ssZ.
    :paramtype start_time_utc: str
    :param end_time_utc: The end time of a lookup query in ISO UTC yyyy-MM-ddTHH:mm:ssZ.
    :paramtype end_time_utc: str
    :param timeout: The server timeout for performing the operation in seconds. This timeout
        specifies the time duration that the client is willing to wait for the requested operation to
        complete. The default value for this parameter is 60 seconds. Default value is 60.
    :paramtype timeout: long
    :param events_types_filter: This is a comma separated string specifying the types of
        FabricEvents that should only be included in the response. Default value is None.
    :paramtype events_types_filter: str
    :param exclude_analysis_events: This param disables the retrieval of AnalysisEvents if true
        is passed. Default value is None.
    :paramtype exclude_analysis_events: bool
    :param skip_correlation_lookup: This param disables the search of CorrelatedEvents
        information if true is passed. otherwise the CorrelationEvents get processed and
        HasCorrelatedEvents field in every FabricEvent gets populated. Default value is None.
        """
    return client.get_application_event_list(application_id, start_time_utc=start_time_utc, end_time_utc=end_time_utc, events_types_filter=events_types_filter, 
                                              exclude_analysis_events=exclude_analysis_events, 
                                              skip_correlation_lookup=skip_correlation_lookup, timeout=timeout)

def get_services_event_list(client, start_time_utc, end_time_utc, events_types_filter=None, exclude_analysis_events=None, skip_correlation_lookup=None, timeout=60):
    """Gets all Service-related events.

    The response is list of Service event objects.

    :param start_time_utc: The start time of a lookup query in ISO UTC yyyy-MM-ddTHH:mm:ssZ.
    :paramtype start_time_utc: str
    :param end_time_utc: The end time of a lookup query in ISO UTC yyyy-MM-ddTHH:mm:ssZ.
    :paramtype end_time_utc: str
    :param timeout: The server timeout for performing the operation in seconds. This timeout
        specifies the time duration that the client is willing to wait for the requested operation to
        complete. The default value for this parameter is 60 seconds. Default value is 60.
    :paramtype timeout: long
    :param events_types_filter: This is a comma separated string specifying the types of
        FabricEvents that should only be included in the response. Default value is None.
    :paramtype events_types_filter: str
    :param exclude_analysis_events: This param disables the retrieval of AnalysisEvents if true
        is passed. Default value is None.
    :paramtype exclude_analysis_events: bool
    :param skip_correlation_lookup: This param disables the search of CorrelatedEvents
        information if true is passed. otherwise the CorrelationEvents get processed and
        HasCorrelatedEvents field in every FabricEvent gets populated. Default value is None.
        """
    return client.get_services_event_list(start_time_utc=start_time_utc, end_time_utc=end_time_utc, events_types_filter=events_types_filter, 
                                              exclude_analysis_events=exclude_analysis_events, 
                                              skip_correlation_lookup=skip_correlation_lookup, timeout=timeout)

def get_service_event_list(client, service_id, start_time_utc, end_time_utc, events_types_filter=None, exclude_analysis_events=None, skip_correlation_lookup=None, timeout=60):
    """Gets all Service-related events for a specific node.

    The response is list of Service event objects.

    :param service_id: The identity of the service. This ID is typically the full name of the
        service without the 'fabric:' URI scheme.
        Starting from version 6.0, hierarchical names are delimited with the "~" character.
        For example, if the service name is "fabric:/myapp/app1/svc1", the service identity would be
        "myapp~app1~svc1" in 6.0+ and "myapp/app1/svc1" in previous versions.
    :type service_id: str
    :param start_time_utc: The start time of a lookup query in ISO UTC yyyy-MM-ddTHH:mm:ssZ.
    :paramtype start_time_utc: str
    :param end_time_utc: The end time of a lookup query in ISO UTC yyyy-MM-ddTHH:mm:ssZ.
    :paramtype end_time_utc: str
    :param timeout: The server timeout for performing the operation in seconds. This timeout
        specifies the time duration that the client is willing to wait for the requested operation to
        complete. The default value for this parameter is 60 seconds. Default value is 60.
    :paramtype timeout: long
    :param events_types_filter: This is a comma separated string specifying the types of
        FabricEvents that should only be included in the response. Default value is None.
    :paramtype events_types_filter: str
    :param exclude_analysis_events: This param disables the retrieval of AnalysisEvents if true
        is passed. Default value is None.
    :paramtype exclude_analysis_events: bool
    :param skip_correlation_lookup: This param disables the search of CorrelatedEvents
        information if true is passed. otherwise the CorrelationEvents get processed and
        HasCorrelatedEvents field in every FabricEvent gets populated. Default value is None.
        """
    return client.get_service_event_list(service_id, start_time_utc=start_time_utc, end_time_utc=end_time_utc, events_types_filter=events_types_filter, 
                                              exclude_analysis_events=exclude_analysis_events, 
                                              skip_correlation_lookup=skip_correlation_lookup, timeout=timeout)
                                              
def get_partitions_event_list(client, start_time_utc, end_time_utc, events_types_filter=None, exclude_analysis_events=None, skip_correlation_lookup=None, timeout=60):
    """Gets all Partition-related events.

    The response is list of Partition event objects.

    :param start_time_utc: The start time of a lookup query in ISO UTC yyyy-MM-ddTHH:mm:ssZ.
    :paramtype start_time_utc: str
    :param end_time_utc: The end time of a lookup query in ISO UTC yyyy-MM-ddTHH:mm:ssZ.
    :paramtype end_time_utc: str
    :param timeout: The server timeout for performing the operation in seconds. This timeout
        specifies the time duration that the client is willing to wait for the requested operation to
        complete. The default value for this parameter is 60 seconds. Default value is 60.
    :paramtype timeout: long
    :param events_types_filter: This is a comma separated string specifying the types of
        FabricEvents that should only be included in the response. Default value is None.
    :paramtype events_types_filter: str
    :param exclude_analysis_events: This param disables the retrieval of AnalysisEvents if true
        is passed. Default value is None.
    :paramtype exclude_analysis_events: bool
    :param skip_correlation_lookup: This param disables the search of CorrelatedEvents
        information if true is passed. otherwise the CorrelationEvents get processed and
        HasCorrelatedEvents field in every FabricEvent gets populated. Default value is None.
        """
    return client.get_partitions_event_list(start_time_utc=start_time_utc, end_time_utc=end_time_utc, events_types_filter=events_types_filter, 
                                              exclude_analysis_events=exclude_analysis_events, 
                                              skip_correlation_lookup=skip_correlation_lookup, timeout=timeout)
                                              
def get_partition_event_list(client, partition_id, start_time_utc, end_time_utc, events_types_filter=None, exclude_analysis_events=None, skip_correlation_lookup=None, timeout=60):
    """Gets all Partition-related events for a specific partition.

    The response is list of Partition event objects.

    :param partition_id: The identity of the partition.
    :type partition_id: str
    :param start_time_utc: The start time of a lookup query in ISO UTC yyyy-MM-ddTHH:mm:ssZ.
    :paramtype start_time_utc: str
    :param end_time_utc: The end time of a lookup query in ISO UTC yyyy-MM-ddTHH:mm:ssZ.
    :paramtype end_time_utc: str
    :param timeout: The server timeout for performing the operation in seconds. This timeout
        specifies the time duration that the client is willing to wait for the requested operation to
        complete. The default value for this parameter is 60 seconds. Default value is 60.
    :paramtype timeout: long
    :param events_types_filter: This is a comma separated string specifying the types of
        FabricEvents that should only be included in the response. Default value is None.
    :paramtype events_types_filter: str
    :param exclude_analysis_events: This param disables the retrieval of AnalysisEvents if true
        is passed. Default value is None.
    :paramtype exclude_analysis_events: bool
    :param skip_correlation_lookup: This param disables the search of CorrelatedEvents
        information if true is passed. otherwise the CorrelationEvents get processed and
        HasCorrelatedEvents field in every FabricEvent gets populated. Default value is None.
        """
    return client.get_partition_event_list(partition_id, start_time_utc=start_time_utc, end_time_utc=end_time_utc, events_types_filter=events_types_filter, 
                                              exclude_analysis_events=exclude_analysis_events, 
                                              skip_correlation_lookup=skip_correlation_lookup, timeout=timeout)

def get_partition_replicas_event_list(client, partition_id, start_time_utc, end_time_utc, events_types_filter=None, exclude_analysis_events=None, skip_correlation_lookup=None, timeout=60):
    """Gets all Partition Replica-related events for a specific replica.

    The response is list of Partition Replica-related event objects.

    :param partition_id: The identity of the partition.
    :type partition_id: str
    :param start_time_utc: The start time of a lookup query in ISO UTC yyyy-MM-ddTHH:mm:ssZ.
    :paramtype start_time_utc: str
    :param end_time_utc: The end time of a lookup query in ISO UTC yyyy-MM-ddTHH:mm:ssZ.
    :paramtype end_time_utc: str
    :param timeout: The server timeout for performing the operation in seconds. This timeout
        specifies the time duration that the client is willing to wait for the requested operation to
        complete. The default value for this parameter is 60 seconds. Default value is 60.
    :paramtype timeout: long
    :param events_types_filter: This is a comma separated string specifying the types of
        FabricEvents that should only be included in the response. Default value is None.
    :paramtype events_types_filter: str
    :param exclude_analysis_events: This param disables the retrieval of AnalysisEvents if true
        is passed. Default value is None.
    :paramtype exclude_analysis_events: bool
    :param skip_correlation_lookup: This param disables the search of CorrelatedEvents
        information if true is passed. otherwise the CorrelationEvents get processed and
        HasCorrelatedEvents field in every FabricEvent gets populated. Default value is None.
        """
    return client.get_partition_replicas_event_list(partition_id, start_time_utc=start_time_utc, end_time_utc=end_time_utc, events_types_filter=events_types_filter, 
                                              exclude_analysis_events=exclude_analysis_events, 
                                              skip_correlation_lookup=skip_correlation_lookup, timeout=timeout)
                                              
def get_partition_replica_event_list(client, partition_id, replica_id, start_time_utc, end_time_utc, events_types_filter=None, exclude_analysis_events=None, skip_correlation_lookup=None, timeout=60):
    """Gets all Partition Replica-related events.

    The response is list of Partition Replica-related objects.

    :param partition_id: The identity of the partition.
    :type partition_id: str
    :param replica_id: The identifier of the replica.
    :type replica_id: str
    :param start_time_utc: The start time of a lookup query in ISO UTC yyyy-MM-ddTHH:mm:ssZ.
    :paramtype start_time_utc: str
    :param end_time_utc: The end time of a lookup query in ISO UTC yyyy-MM-ddTHH:mm:ssZ.
    :paramtype end_time_utc: str
    :param timeout: The server timeout for performing the operation in seconds. This timeout
        specifies the time duration that the client is willing to wait for the requested operation to
        complete. The default value for this parameter is 60 seconds. Default value is 60.
    :paramtype timeout: long
    :param events_types_filter: This is a comma separated string specifying the types of
        FabricEvents that should only be included in the response. Default value is None.
    :paramtype events_types_filter: str
    :param exclude_analysis_events: This param disables the retrieval of AnalysisEvents if true
        is passed. Default value is None.
    :paramtype exclude_analysis_events: bool
    :param skip_correlation_lookup: This param disables the search of CorrelatedEvents
        information if true is passed. otherwise the CorrelationEvents get processed and
        HasCorrelatedEvents field in every FabricEvent gets populated. Default value is None.
        """
    return client.get_partition_replica_event_list(partition_id, replica_id, start_time_utc=start_time_utc, end_time_utc=end_time_utc, events_types_filter=events_types_filter, 
                                              exclude_analysis_events=exclude_analysis_events, 
                                              skip_correlation_lookup=skip_correlation_lookup, timeout=timeout)