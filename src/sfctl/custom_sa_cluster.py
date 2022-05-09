# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------

def get_cluster_configuration(client, configuration_api_version, timeout=60):
    """Get the Service Fabric standalone cluster configuration.

    The cluster configuration contains properties of the cluster that include different node types
    on the cluster,
    security configurations, fault, and upgrade domain topologies, etc.

    :param configuration_api_version: The API version of the Standalone cluster json
        configuration.
    :paramtype configuration_api_version: str
    """
    return client.get_cluster_configuration(configuration_api_version=configuration_api_version, timeout=timeout)