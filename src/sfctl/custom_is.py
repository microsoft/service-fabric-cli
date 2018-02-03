# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Custom commands for the Service Fabric infrastructure service support"""

def is_command(client, command_input, service_id=None, timeout=60):
    """Invokes an administrative command on the given Infrastructure Service
    instance.

    For clusters that have one or more instances of the Infrastructure
    Service configured,
    this API provides a way to send infrastructure-specific commands to a
    particular
    instance of the Infrastructure Service.
    Available commands and their corresponding response formats vary
    depending upon
    the infrastructure on which the cluster is running.
    This API supports the Service Fabric platform; it is not meant to be
    used directly from your code.

    :param command_input: The text of the command to be invoked. The content of
        the command is infrastructure-specific.
    :type command_input: str
    :param service_id: The identity of the infrastructure service. This is
        the full name of the infrastructure service without the 'fabric:' URI
        scheme. This parameter required only for the cluster that have more
        than one instance of infrastructure service running.
    :type service_id: str
    :param timeout: The server timeout for performing the operation in
        seconds. This specifies the time duration that the client is willing
        to wait for the requested operation to complete. The default value for
        this parameter is 60 seconds.
    :type timeout: long
    :param dict custom_headers: headers that will be added to the request
    :param bool raw: returns the direct response alongside the
        deserialized response
    :param operation_config: :ref:`Operation configuration
        overrides<msrest:optionsforoperations>`.
    :return: str or ClientRawResponse if raw=true
    :rtype: str or ~msrest.pipeline.ClientRawResponse
    :raises:
        :class:
        `FabricErrorException<azure.servicefabric.models.FabricErrorException>`
    """
    client.invoke_infrastructure_command(command_input, service_id, timeout)

def is_query(client, command_input, service_id=None, timeout=60):
    """Invokes a read-only query on the given infrastructure service instance.

    For clusters that have one or more instances of the Infrastructure
    Service configured,
    this API provides a way to send infrastructure-specific queries to a
    particular
    instance of the Infrastructure Service.
    Available commands and their corresponding response formats vary
    depending upon
    the infrastructure on which the cluster is running.
    This API supports the Service Fabric platform; it is not meant to be
    used directly from your code.

    :param command_input: The text of the command to be invoked. The content of
        the command is infrastructure-specific.
    :type command_input: str
    :param service_id: The identity of the infrastructure service. This is
        the full name of the infrastructure service without the 'fabric:' URI
        scheme. This parameter required only for the cluster that have more
        than one instance of infrastructure service running.
    :type service_id: str
    :param timeout: The server timeout for performing the operation in
        seconds. This specifies the time duration that the client is willing
        to wait for the requested operation to complete. The default value for
        this parameter is 60 seconds.
    :type timeout: long
    :param dict custom_headers: headers that will be added to the request
    :param bool raw: returns the direct response alongside the
        deserialized response
    :param operation_config: :ref:`Operation configuration
        overrides<msrest:optionsforoperations>`.
    :return: str or ClientRawResponse if raw=true
    :rtype: str or ~msrest.pipeline.ClientRawResponse
    :raises:
        :class:
        `FabricErrorException<azure.servicefabric.models.FabricErrorException>`
    """
    client.invoke_infrastructure_query(command_input, service_id, timeout)
