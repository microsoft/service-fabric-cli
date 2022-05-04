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

def disable_node(client, node_name, deactivation_intent, timeout=60):
    """Deactivate a Service Fabric cluster node with the specified deactivation.

    :param str node_name: The name of the node
    :param str deactivation_intent: Describes the intent or reason for deactivating the node.
    """
    payload = {
        "DeactivationIntent": deactivation_intent
    }

    client.disable_node(node_name, payload, timeout=timeout)


def restart_node(client, node_name, node_instance_id=0, create_fabric_dump=False,  timeout=60):
    """Restarts a Service Fabric cluster node.

    :param str node_name: The name of the node
    :param str node_instance_id: The instance ID of the target node. If instance ID is specified the
                             node is restarted only if it matches with the current instance of the
                             node. A default value of "0" would match any instance ID. The instance
                             ID can be obtained using get node query
    :param str create_fabric_dump: Specify True to create a dump of the fabric node process. This is case sensitive. Default: False
    """
    payload = {
        "CreateFabricDump": create_fabric_dump,
        "NodeInstanceId": node_instance_id
    }

    client.restart_node(node_name, payload, timeout=timeout)