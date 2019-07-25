# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Custom commands for the Service Fabric container support"""

from __future__ import print_function
import json
from azure.servicefabric.models import ContainerApiRequestBody

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
        timeout=60):
    """Invoke container API on a cluster node"""

    request_body = ContainerApiRequestBody(
        uri_path=container_api_uri_path,
        http_verb=container_api_http_verb,
        content_type=container_api_content_type,
        body=container_api_body)

    response = client.invoke_container_api(
        node_name,
        application_id,
        service_manifest_name,
        code_package_name,
        code_package_instance_id,
        request_body,
        timeout)

    print(format_response(response))

def logs( # pylint: disable=too-many-arguments
        client,
        node_name,
        application_id,
        service_manifest_name,
        code_package_name,
        code_package_instance_id,
        tail=None,
        timeout=60):
    """Get container logs"""

    uri_path = '/containers/{id}/logs?stdout=true&stderr=true'
    if tail:
        uri_path += '&tail={}'.format(tail)

    request_body = ContainerApiRequestBody(uri_path=uri_path)

    response = client.invoke_container_api(
        node_name,
        application_id,
        service_manifest_name,
        code_package_name,
        code_package_instance_id,
        request_body,
        timeout)

    if response:
        if response.container_api_result.status == 200:
            print(response.container_api_result.body)
        else:
            print(format_response(response))

def format_response(response):
    """ pretty print json response """
    # Note: We are not printing the entire response type
    # (azure.servicefabric.models.container_api_response_py3.ContainerApiResponse), but instead,
    # printing only ContainerApiResult because it contains all the data, and we avoid the need
    # to use jsonpickle encoding
    if response and response.container_api_result:
        return json.dumps(response.container_api_result.__dict__, sort_keys=True, indent=4)
    return None
