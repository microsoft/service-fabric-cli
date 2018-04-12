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
        and entities. This version is compatible with Service Fabric 6.2
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
    short-summary: Create, delete, and manage applications and application
        types
"""

helps['chaos'] = """
    type: group
    short-summary: Start, stop and report on the chaos test service
"""

helps['chaos schedule'] = """
    type: group
    short-summary: Get and set the chaos schedule
"""

helps['cluster'] = """
    type: group
    short-summary: Select, manage and operate Service Fabric clusters
"""

helps['compose'] = """
    type: group
    short-summary: Create, delete and manage Docker Compose applications
"""

helps['container'] = """
    type: group
    short-summary: run container related commands on a cluster node
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