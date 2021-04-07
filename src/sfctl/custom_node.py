# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Commands related to Service Fabric Node commands for node tagging"""

def add_node_tags(client, node_name, tags):
    """Add the corresponding tags to a node"""

    client.add_node_tags(node_name, tags.split(","))


def remove_node_tags(client, node_name, tags):
    """remove the corresponding tags to a node"""

    client.remove_node_tags(node_name, tags.split(","))
