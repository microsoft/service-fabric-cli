# pylint: disable=too-many-lines
# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------
from typing import TYPE_CHECKING

from msrest import Serializer

from azure.core.exceptions import ClientAuthenticationError, HttpResponseError, ResourceExistsError, ResourceNotFoundError, map_error
from azure.core.pipeline import PipelineResponse
from azure.core.pipeline.transport import HttpResponse
from azure.core.rest import HttpRequest
from azure.core.tracing.decorator import distributed_trace
from azure.mgmt.core.exceptions import ARMErrorFormat

from .. import models as _models
from .._vendor import _convert_request, _format_url_section

if TYPE_CHECKING:
    # pylint: disable=unused-import,ungrouped-imports
    from typing import Any, Callable, Dict, Optional, TypeVar, Union
    T = TypeVar('T')
    ClsType = Optional[Callable[[PipelineResponse[HttpRequest, HttpResponse], T, Dict[str, Any]], Any]]

_SERIALIZER = Serializer()
_SERIALIZER.client_side_validation = False
# fmt: off

def build_get_container_logs_request(
    application_resource_name,  # type: str
    service_resource_name,  # type: str
    replica_name,  # type: str
    code_package_name,  # type: str
    **kwargs  # type: Any
):
    # type: (...) -> HttpRequest
    api_version = kwargs.pop('api_version', "9.0.0.46")  # type: str
    tail = kwargs.pop('tail', None)  # type: Optional[str]

    accept = "application/json"
    # Construct URL
    _url = kwargs.pop("template_url", "/Resources/Applications/{applicationResourceName}/Services/{serviceResourceName}/Replicas/{replicaName}/CodePackages/{codePackageName}/Logs")  # pylint: disable=line-too-long
    path_format_arguments = {
        "applicationResourceName": _SERIALIZER.url("application_resource_name", application_resource_name, 'str', skip_quote=True),
        "serviceResourceName": _SERIALIZER.url("service_resource_name", service_resource_name, 'str', skip_quote=True),
        "replicaName": _SERIALIZER.url("replica_name", replica_name, 'str', skip_quote=True),
        "codePackageName": _SERIALIZER.url("code_package_name", code_package_name, 'str'),
    }

    _url = _format_url_section(_url, **path_format_arguments)

    # Construct parameters
    _query_parameters = kwargs.pop("params", {})  # type: Dict[str, Any]
    _query_parameters['api-version'] = _SERIALIZER.query("api_version", api_version, 'str')
    if tail is not None:
        _query_parameters['Tail'] = _SERIALIZER.query("tail", tail, 'str')

    # Construct headers
    _header_parameters = kwargs.pop("headers", {})  # type: Dict[str, Any]
    _header_parameters['Accept'] = _SERIALIZER.header("accept", accept, 'str')

    return HttpRequest(
        method="GET",
        url=_url,
        params=_query_parameters,
        headers=_header_parameters,
        **kwargs
    )

# fmt: on
class MeshCodePackageOperations(object):
    """
    .. warning::
        **DO NOT** instantiate this class directly.

        Instead, you should access the following operations through
        :class:`~azure.servicefabric.ServiceFabricClientAPIs`'s
        :attr:`mesh_code_package` attribute.
    """

    models = _models

    def __init__(self, *args, **kwargs):
        args = list(args)
        self._client = args.pop(0) if args else kwargs.pop("client")
        self._config = args.pop(0) if args else kwargs.pop("config")
        self._serialize = args.pop(0) if args else kwargs.pop("serializer")
        self._deserialize = args.pop(0) if args else kwargs.pop("deserializer")


    @distributed_trace
    def get_container_logs(
        self,
        application_resource_name,  # type: str
        service_resource_name,  # type: str
        replica_name,  # type: str
        code_package_name,  # type: str
        tail=None,  # type: Optional[str]
        **kwargs  # type: Any
    ):
        # type: (...) -> "_models.ContainerLogs"
        """Gets the logs from the container.

        Gets the logs for the container of the specified code package of the service replica.

        :param application_resource_name: The identity of the application.
        :type application_resource_name: str
        :param service_resource_name: The identity of the service.
        :type service_resource_name: str
        :param replica_name: Service Fabric replica name.
        :type replica_name: str
        :param code_package_name: The name of code package of the service.
        :type code_package_name: str
        :param tail: Number of lines to show from the end of the logs. Default is 100. 'all' to show
         the complete logs.
        :type tail: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: ContainerLogs, or the result of cls(response)
        :rtype: ~azure.servicefabric.models.ContainerLogs
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["_models.ContainerLogs"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))

        api_version = kwargs.pop('api_version', "9.0.0.46")  # type: str

        
        request = build_get_container_logs_request(
            application_resource_name=application_resource_name,
            service_resource_name=service_resource_name,
            replica_name=replica_name,
            code_package_name=code_package_name,
            api_version=api_version,
            tail=tail,
            template_url=self.get_container_logs.metadata['url'],
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        pipeline_response = self._client._pipeline.run(  # pylint: disable=protected-access
            request,
            stream=False,
            **kwargs
        )
        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.FabricError, pipeline_response)
            raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

        deserialized = self._deserialize('ContainerLogs', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    get_container_logs.metadata = {'url': "/Resources/Applications/{applicationResourceName}/Services/{serviceResourceName}/Replicas/{replicaName}/CodePackages/{codePackageName}/Logs"}  # type: ignore

