# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Commands related to Service Fabric Mesh secret value commands and operations"""


def get_secret_value(client, secret_resource_name, secret_value_resource_name, show_value):
    """structure is meant to make testing easier because testing
        does not assume for 2 requests from one command"""
    secret_value = None
    if show_value:
        secret_value = client.show(secret_resource_name, secret_value_resource_name)

    secret_data = client.get(secret_resource_name, secret_value_resource_name)

    if secret_value:
        secret_data.value = secret_value['value']
    return secret_data
