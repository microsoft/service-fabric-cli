# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Help documentation for Service Fabric groups"""

from knack.help_files import helps

helps[''] = """
    type: group
    short-summary: Commands for managing Service Fabric clusters
        and entities. This version is compatible with Service Fabric 7.1
        runtime.
    long-summary: Commands follow the noun-verb pattern. See subgroups for more
        information.
"""

helps['rpm'] = """
    type: group
    short-summary: Query and send commands to the repair manager service
"""

helps['sa-cluster'] = """
    type: group
    short-summary: Manage stand-alone Service Fabric clusters
"""

helps['application'] = """
    type: group
    short-summary: Create, delete, and manage applications and application types
"""

helps['chaos'] = """
    type: group
    short-summary: Start, stop, and report on the chaos test service
"""

helps['chaos schedule'] = """
    type: group
    short-summary: Get and set the chaos schedule
"""

helps['cluster'] = """
    type: group
    short-summary: Select, manage, and operate Service Fabric clusters
"""

helps['compose'] = """
    type: group
    short-summary: Create, delete, and manage Docker Compose applications
"""

helps['container'] = """
    type: group
    short-summary: Run container related commands on a cluster node
"""

helps['is'] = """
    type: group
    short-summary: Query and send commands to the infrastructure service
"""

helps['node'] = """
    type: group
    short-summary: Manage the nodes that form a cluster
"""

helps['partition'] = """
    type: group
    short-summary: Query and manage partitions for any service
"""

helps['replica'] = """
    type: group
    short-summary: Manage the replicas that belong to service partitions
"""

helps['service'] = """
    type: group
    short-summary: Create, delete and manage service, service types and
        service packages
"""

helps['store'] = """
    type: group
    short-summary: Perform basic file level operations on the cluster image
        store
"""

helps['property'] = """
    type: group
    short-summary: Store and query properties under Service Fabric names
"""

helps['settings'] = """
    type: group
    short-summary: Configure settings local to this instance of sfctl
"""

helps['settings telemetry'] = """
    type: group
    short-summary: Configure telemetry settings local to this instance of sfctl
    long-summary: Sfctl telemetry collects command name without parameters provided or their values,
        sfctl version, OS type, python version, the success or failure of the command,
        the error message returned
"""

helps['events'] = """
    type: group
    short-summary: Retrieve events from the events store (if EventStore service is already installed)
    long-summary: 'The EventStore system service can be added through a config upgrade to any SFRP cluster running >=6.4.
        Please check the following url:
        https://docs.microsoft.com/azure/service-fabric/service-fabric-diagnostics-eventstore'
"""
