# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Custom commands for the Service Fabric infrastructure service support"""


def is_command(client, command_input, service_id=None, timeout=60):
    """Invokes an administrative command on the given Infrastructure Service
    instance.
    """
    client.invoke_infrastructure_command(command=command_input, service_id=service_id, timeout=timeout)


def is_query(client, command_input, service_id=None, timeout=60):
    """Invokes a read-only query on the given infrastructure service instance.
    """
    client.invoke_infrastructure_query(command=command_input, service_id=service_id, timeout=timeout)


def force_approve_repair_task(client, task_id, version, timeout=60):
    """Forces the approval of the given repair task.

    :param str task_id: The ID of the repair task.
    :param str version: The current version number of the repair task. If non-zero, then the
    request will only succeed if this value matches the actual current
    version of the repair task. If zero, then no version check is performed.
    """
    payload = {
        "TaskId": task_id,
        "Version": version
    }
    client.force_approve_repair_task(payload, timeout=timeout)


def delete_repair_task(client, task_id, version, timeout=60):
    """This API supports the Service Fabric platform; it is not meant to be used directly from your code.

    :param str task_id: The ID of the repair task.
    :param str version: The current version number of the repair task. If non-zero, then the
    request will only succeed if this value matches the actual current
    version of the repair task. If zero, then no version check is performed.
    """
    payload = {
        "TaskId": task_id,
        "Version": version
    }
    client.delete_repair_task(payload, timeout=timeout)

def get_repair_task_list(client, task_id_filter=None, state_filter=None, executor_filter=None):
    """Gets a list of repair tasks matching the given filters.

    This API supports the Service Fabric platform; it is not meant to be used directly from your
    code.

    :param task_id_filter: The repair task ID prefix to be matched. Default value is None.
    :paramtype task_id_filter: str
    :param state_filter: A bitwise-OR of the following values, specifying which task states
        should be included in the result list.


        * 1 - Created
        * 2 - Claimed
        * 4 - Preparing
        * 8 - Approved
        * 16 - Executing
        * 32 - Restoring
        * 64 - Completed. Default value is None.
    :paramtype state_filter: int
    :param executor_filter: The name of the repair executor whose claimed tasks should be
        included in the list. Default value is None.
        """

    return client.get_repair_task_list(task_id_filter=task_id_filter, state_filter=state_filter, executor_filter=executor_filter)