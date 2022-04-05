# pylint: disable=too-many-lines
# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------
from typing import Any, Callable, Dict, Optional, TypeVar

from azure.core.exceptions import ClientAuthenticationError, HttpResponseError, ResourceExistsError, ResourceNotFoundError, map_error
from azure.core.pipeline import PipelineResponse
from azure.core.pipeline.transport import AsyncHttpResponse
from azure.core.rest import HttpRequest
from azure.core.tracing.decorator_async import distributed_trace_async
from azure.mgmt.core.exceptions import ARMErrorFormat

from ... import models as _models
from ..._vendor import _convert_request
from ...operations._mesh_service_operations import build_get_request, build_list_request
T = TypeVar('T')
ClsType = Optional[Callable[[PipelineResponse[HttpRequest, AsyncHttpResponse], T, Dict[str, Any]], Any]]

class MeshServiceOperations:
    """
    .. warning::
        **DO NOT** instantiate this class directly.

        Instead, you should access the following operations through
        :class:`~azure.servicefabric.aio.ServiceFabricClientAPIs`'s
        :attr:`mesh_service` attribute.
    """

    models = _models

    def __init__(self, *args, **kwargs) -> None:
        args = list(args)
        self._client = args.pop(0) if args else kwargs.pop("client")
        self._config = args.pop(0) if args else kwargs.pop("config")
        self._serialize = args.pop(0) if args else kwargs.pop("serializer")
        self._deserialize = args.pop(0) if args else kwargs.pop("deserializer")


    @distributed_trace_async
    async def get(
        self,
        application_resource_name: str,
        service_resource_name: str,
        **kwargs: Any
    ) -> "_models.ServiceResourceDescription":
        """Gets the Service resource with the given name.

        Gets the information about the Service resource with the given name. The information include
        the description and other properties of the Service.

        :param application_resource_name: The identity of the application.
        :type application_resource_name: str
        :param service_resource_name: The identity of the service.
        :type service_resource_name: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: ServiceResourceDescription, or the result of cls(response)
        :rtype: ~azure.servicefabric.models.ServiceResourceDescription
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["_models.ServiceResourceDescription"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))

        api_version = kwargs.pop('api_version', "8.2.0.46")  # type: str

        
        request = build_get_request(
            application_resource_name=application_resource_name,
            service_resource_name=service_resource_name,
            api_version=api_version,
            template_url=self.get.metadata['url'],
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        pipeline_response = await self._client._pipeline.run(  # pylint: disable=protected-access
            request,
            stream=False,
            **kwargs
        )
        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.FabricError, pipeline_response)
            raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

        deserialized = self._deserialize('ServiceResourceDescription', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    get.metadata = {'url': "/Resources/Applications/{applicationResourceName}/Services/{serviceResourceName}"}  # type: ignore


    @distributed_trace_async
    async def list(
        self,
        application_resource_name: str,
        **kwargs: Any
    ) -> "_models.PagedServiceResourceDescriptionList":
        """Lists all the service resources.

        Gets the information about all services of an application resource. The information include the
        description and other properties of the Service.

        :param application_resource_name: The identity of the application.
        :type application_resource_name: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: PagedServiceResourceDescriptionList, or the result of cls(response)
        :rtype: ~azure.servicefabric.models.PagedServiceResourceDescriptionList
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["_models.PagedServiceResourceDescriptionList"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))

        api_version = kwargs.pop('api_version', "8.2.0.46")  # type: str

        
        request = build_list_request(
            application_resource_name=application_resource_name,
            api_version=api_version,
            template_url=self.list.metadata['url'],
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        pipeline_response = await self._client._pipeline.run(  # pylint: disable=protected-access
            request,
            stream=False,
            **kwargs
        )
        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.FabricError, pipeline_response)
            raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

        deserialized = self._deserialize('PagedServiceResourceDescriptionList', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    list.metadata = {'url': "/Resources/Applications/{applicationResourceName}/Services"}  # type: ignore

