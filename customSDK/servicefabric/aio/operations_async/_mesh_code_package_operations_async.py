# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

import uuid
from msrest.pipeline import ClientRawResponse

from ... import models


class MeshCodePackageOperations:
    """MeshCodePackageOperations async operations.

    You should not instantiate directly this class, but create a Client instance that will create it for you and attach it as attribute.

    :param client: Client for service requests.
    :param config: Configuration of service client.
    :param serializer: An object model serializer.
    :param deserializer: An object model deserializer.
    :ivar api_version: The version of the API. This parameter is required and its value must be '6.4-preview'. Constant value: "6.4-preview".
    """

    models = models

    def __init__(self, client, config, serializer, deserializer) -> None:

        self._client = client
        self._serialize = serializer
        self._deserialize = deserializer
        self.api_version = "6.4-preview"

        self.config = config

    async def get_container_logs(
            self, application_resource_name, service_resource_name, replica_name, code_package_name, tail=None, *, custom_headers=None, raw=False, **operation_config):
        """Gets the logs from the container.

        Gets the logs for the container of the specified code package of the
        service replica.

        :param application_resource_name: The identity of the application.
        :type application_resource_name: str
        :param service_resource_name: The identity of the service.
        :type service_resource_name: str
        :param replica_name: Service Fabric replica name.
        :type replica_name: str
        :param code_package_name: The name of code package of the service.
        :type code_package_name: str
        :param tail: Number of lines to show from the end of the logs. Default
         is 100. 'all' to show the complete logs.
        :type tail: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: ContainerLogs or ClientRawResponse if raw=true
        :rtype: ~azure.servicefabric.models.ContainerLogs or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`FabricErrorException<azure.servicefabric.models.FabricErrorException>`
        """
        # Construct URL
        url = self.get_container_logs.metadata['url']
        path_format_arguments = {
            'applicationResourceName': self._serialize.url("application_resource_name", application_resource_name, 'str', skip_quote=True),
            'serviceResourceName': self._serialize.url("service_resource_name", service_resource_name, 'str', skip_quote=True),
            'replicaName': self._serialize.url("replica_name", replica_name, 'str', skip_quote=True),
            'codePackageName': self._serialize.url("code_package_name", code_package_name, 'str')
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}
        query_parameters['api-version'] = self._serialize.query("self.api_version", self.api_version, 'str')
        if tail is not None:
            query_parameters['Tail'] = self._serialize.query("tail", tail, 'str')

        # Construct headers
        header_parameters = {}
        header_parameters['Accept'] = 'application/json'
        if self.config.generate_client_request_id:
            header_parameters['x-ms-client-request-id'] = str(uuid.uuid1())
        if custom_headers:
            header_parameters.update(custom_headers)
        if self.config.accept_language is not None:
            header_parameters['accept-language'] = self._serialize.header("self.config.accept_language", self.config.accept_language, 'str')

        # Construct and send request
        request = self._client.get(url, query_parameters, header_parameters)
        response = await self._client.async_send(request, stream=False, **operation_config)

        if response.status_code not in [200]:
            raise models.FabricErrorException(self._deserialize, response)

        deserialized = None
        if response.status_code == 200:
            deserialized = self._deserialize('ContainerLogs', response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized
    get_container_logs.metadata = {'url': '/Resources/Applications/{applicationResourceName}/Services/{serviceResourceName}/Replicas/{replicaName}/CodePackages/{codePackageName}/Logs'}
