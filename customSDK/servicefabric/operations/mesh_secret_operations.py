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

from .. import models


class MeshSecretOperations(object):
    """MeshSecretOperations operations.

    :param client: Client for service requests.
    :param config: Configuration of service client.
    :param serializer: An object model serializer.
    :param deserializer: An object model deserializer.
    :ivar api_version: The version of the API. This parameter is required and its value must be '6.4-preview'. Constant value: "6.4-preview".
    """

    models = models

    def __init__(self, client, config, serializer, deserializer):

        self._client = client
        self._serialize = serializer
        self._deserialize = deserializer
        self.api_version = "6.4-preview"

        self.config = config

    def create_or_update(
            self, secret_resource_name, properties, name, custom_headers=None, raw=False, **operation_config):
        """Creates or updates a Secret resource.

        Creates a Secret resource with the specified name, description and
        properties. If Secret resource with the same name exists, then it is
        updated with the specified description and properties. Once created,
        the kind and contentType of a secret resource cannot be updated.

        :param secret_resource_name: The name of the secret resource.
        :type secret_resource_name: str
        :param properties: Describes the properties of a secret resource.
        :type properties: ~azure.servicefabric.models.SecretResourceProperties
        :param name: Name of the Secret resource.
        :type name: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: SecretResourceDescription or ClientRawResponse if raw=true
        :rtype: ~azure.servicefabric.models.SecretResourceDescription or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`FabricErrorException<azure.servicefabric.models.FabricErrorException>`
        """
        secret_resource_description = models.SecretResourceDescription(properties=properties, name=name)

        # Construct URL
        url = self.create_or_update.metadata['url']
        path_format_arguments = {
            'secretResourceName': self._serialize.url("secret_resource_name", secret_resource_name, 'str', skip_quote=True)
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}
        query_parameters['api-version'] = self._serialize.query("self.api_version", self.api_version, 'str')

        # Construct headers
        header_parameters = {}
        header_parameters['Accept'] = 'application/json'
        header_parameters['Content-Type'] = 'application/json; charset=utf-8'
        if self.config.generate_client_request_id:
            header_parameters['x-ms-client-request-id'] = str(uuid.uuid1())
        if custom_headers:
            header_parameters.update(custom_headers)
        if self.config.accept_language is not None:
            header_parameters['accept-language'] = self._serialize.header("self.config.accept_language", self.config.accept_language, 'str')

        # Construct body
        body_content = self._serialize.body(secret_resource_description, 'SecretResourceDescription')

        # Construct and send request
        request = self._client.put(url, query_parameters, header_parameters, body_content)
        response = self._client.send(request, stream=False, **operation_config)

        if response.status_code not in [200, 201, 202]:
            raise models.FabricErrorException(self._deserialize, response)

        deserialized = None

        if response.status_code == 200:
            deserialized = self._deserialize('SecretResourceDescription', response)
        if response.status_code == 201:
            deserialized = self._deserialize('SecretResourceDescription', response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized
    create_or_update.metadata = {'url': '/Resources/Secrets/{secretResourceName}'}

    def get(
            self, secret_resource_name, custom_headers=None, raw=False, **operation_config):
        """Gets the Secret resource with the given name.

        Gets the information about the Secret resource with the given name. The
        information include the description and other properties of the Secret.

        :param secret_resource_name: The name of the secret resource.
        :type secret_resource_name: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: SecretResourceDescription or ClientRawResponse if raw=true
        :rtype: ~azure.servicefabric.models.SecretResourceDescription or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`FabricErrorException<azure.servicefabric.models.FabricErrorException>`
        """
        # Construct URL
        url = self.get.metadata['url']
        path_format_arguments = {
            'secretResourceName': self._serialize.url("secret_resource_name", secret_resource_name, 'str', skip_quote=True)
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}
        query_parameters['api-version'] = self._serialize.query("self.api_version", self.api_version, 'str')

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
        response = self._client.send(request, stream=False, **operation_config)

        if response.status_code not in [200]:
            raise models.FabricErrorException(self._deserialize, response)

        deserialized = None

        if response.status_code == 200:
            deserialized = self._deserialize('SecretResourceDescription', response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized
    get.metadata = {'url': '/Resources/Secrets/{secretResourceName}'}

    def delete(
            self, secret_resource_name, custom_headers=None, raw=False, **operation_config):
        """Deletes the Secret resource.

        Deletes the specified Secret resource and all of its named values.

        :param secret_resource_name: The name of the secret resource.
        :type secret_resource_name: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: None or ClientRawResponse if raw=true
        :rtype: None or ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`FabricErrorException<azure.servicefabric.models.FabricErrorException>`
        """
        # Construct URL
        url = self.delete.metadata['url']
        path_format_arguments = {
            'secretResourceName': self._serialize.url("secret_resource_name", secret_resource_name, 'str', skip_quote=True)
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}
        query_parameters['api-version'] = self._serialize.query("self.api_version", self.api_version, 'str')

        # Construct headers
        header_parameters = {}
        if self.config.generate_client_request_id:
            header_parameters['x-ms-client-request-id'] = str(uuid.uuid1())
        if custom_headers:
            header_parameters.update(custom_headers)
        if self.config.accept_language is not None:
            header_parameters['accept-language'] = self._serialize.header("self.config.accept_language", self.config.accept_language, 'str')

        # Construct and send request
        request = self._client.delete(url, query_parameters, header_parameters)
        response = self._client.send(request, stream=False, **operation_config)

        if response.status_code not in [200, 202, 204]:
            raise models.FabricErrorException(self._deserialize, response)

        if raw:
            client_raw_response = ClientRawResponse(None, response)
            return client_raw_response
    delete.metadata = {'url': '/Resources/Secrets/{secretResourceName}'}

    def list(
            self, custom_headers=None, raw=False, **operation_config):
        """Lists all the secret resources.

        Gets the information about all secret resources in a given resource
        group. The information include the description and other properties of
        the Secret.

        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: PagedSecretResourceDescriptionList or ClientRawResponse if
         raw=true
        :rtype: ~azure.servicefabric.models.PagedSecretResourceDescriptionList
         or ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`FabricErrorException<azure.servicefabric.models.FabricErrorException>`
        """
        # Construct URL
        url = self.list.metadata['url']

        # Construct parameters
        query_parameters = {}
        query_parameters['api-version'] = self._serialize.query("self.api_version", self.api_version, 'str')

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
        response = self._client.send(request, stream=False, **operation_config)

        if response.status_code not in [200]:
            raise models.FabricErrorException(self._deserialize, response)

        deserialized = None

        if response.status_code == 200:
            deserialized = self._deserialize('PagedSecretResourceDescriptionList', response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized
    list.metadata = {'url': '/Resources/Secrets'}
