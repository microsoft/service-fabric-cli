# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Custom commands for the Service Fabric Docker compose support"""

from knack.cli import CLIError

def invoke_container_api(
        client,
        node_name,
        application_id,
        service_manifest_name,
        code_package_name,
        code_package_instance_id,
        container_api_uri_path,
        container_api_http_verb='',
        container_api_content_type='',
        container_api_body='',
        timeout=60,
        custom_headers=None,
        raw=False,
        **operation_config):

    from azure.servicefabric.models import ContainerApiRequestBody

    containerApiRequestBody = ContainerApiRequestBody(
        container_api_uri_path,
        container_api_http_verb,
        container_api_content_type,
        container_api_body)

    response = client.invoke_container_api(
        node_name,
        application_id,
        service_manifest_name,
        code_package_name,
        code_package_instance_id,
        containerApiRequestBody,
        timeout,
        custom_headers,
        raw)

    import jsonpickle
    print(jsonpickle.encode(response, unpicklable=False))