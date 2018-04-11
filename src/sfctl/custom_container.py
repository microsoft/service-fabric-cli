# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Custom commands for the Service Fabric Docker compose support"""

from azure.servicefabric.models import ContainerApiRequestBody
import jsonpickle

def invoke_api( # pylint: disable=too-many-arguments
        client,
        node_name,
        application_id,
        service_manifest_name,
        code_package_name,
        code_package_instance_id,
        container_api_uri_path,
        container_api_http_verb=None,
        container_api_content_type=None,
        container_api_body=None,
        timeout=60,
        custom_headers=None,
        raw=False):
    """Invoke container API on a cluster node"""

    request_body = ContainerApiRequestBody(
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
        request_body,
        timeout,
        custom_headers,
        raw)

    print(jsonpickle.encode(response, unpicklable=False))

def logs( # pylint: disable=too-many-arguments
        client,
        node_name,
        application_id,
        service_manifest_name,
        code_package_name,
        code_package_instance_id,
        tail='',
        timeout=60,
        custom_headers=None,
        raw=False):
    """Get container logs"""

    uri_path = '/containers/{id}/logs?stdout=true&stderr=true'
    if tail:
        uri_path += f'&tail={tail}'

    request_body = ContainerApiRequestBody(uri_path)

    response = client.invoke_container_api(
        node_name,
        application_id,
        service_manifest_name,
        code_package_name,
        code_package_instance_id,
        request_body,
        timeout,
        custom_headers,
        raw)

    if response:
        if response.container_api_result.status == 200:
            print(response.container_api_result.body)
        else:
            print(jsonpickle.encode(response, unpicklable=False))
