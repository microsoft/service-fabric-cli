# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Help documentation for Service Fabric Infrastructure Service commands."""

from knack.help_files import helps

helps['is command'] = """
    type: command
    short-summary: Invokes an administrative command on the given
        Infrastructure Service instance.
    long-summary: For clusters that have one or more instances of
        the Infrastructure Service configured, this API provides a way to
        send infrastructure-specific commands to a particular instance of
        the Infrastructure Service. Available commands and their corresponding
        response formats vary depending upon the infrastructure on which the
        cluster is running. This API supports the Service Fabric platform;
        it is not meant to be used directly from your code.
    parameters:
        - name: --command
          type: string
          short-summary: The text of the command to be invoked. The content of
            the command is infrastructure-specific.
        - name: --service-id
          type: string
          short-summary: The identity of the infrastructure service.
          long-summary: This is the full name of the infrastructure service
            without the 'fabric' URI scheme. This parameter required only for
            the cluster that have more than one instance of infrastructure
            service running.
"""

helps['is query'] = """
    type: command
    short-summary: Invokes a read-only query on the given infrastructure
        service instance.
    long-summary: For clusters that have one or more instances of
        the Infrastructure Service configured, this API provides a way to
        send infrastructure-specific queries to a particular instance of
        the Infrastructure Service. Available commands and their corresponding
        response formats vary depending upon the infrastructure on which the
        cluster is running. This API supports the Service Fabric platform;
        it is not meant to be used directly from your code.
    parameters:
        - name: --command
          type: string
          short-summary: The text of the command to be invoked. The content of
            the command is infrastructure-specific.
        - name: --service-id
          type: string
          short-summary: The identity of the infrastructure service.
          long-summary: This is the full name of the infrastructure service
            without the 'fabric:' URI scheme. This parameter required only for
            the cluster that have more than one instance of infrastructure
            service running.
"""
