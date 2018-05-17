# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Custom commands for the Service Fabric container support"""

from __future__ import print_function
import json
import jsonpickle
from azure.servicefabric.models.container_api_request_body import ContainerApiRequestBody

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
    encoded = jsonpickle.encode(response, unpicklable=False)
    return json.dumps(json.loads(encoded), indent=4)
    