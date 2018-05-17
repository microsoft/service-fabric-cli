# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Custom application type related commands"""

from collections import OrderedDict
from knack.util import CLIError
from sfctl.custom_exceptions import SFCTLInternalException

# We are disabling some W0212 (protected-access) lint warnings in the following function
# because of a problem with the generated SDK that does not allow this
# function to be called upon from within the generated SDK.
# pylint: disable=protected-access

def provision_application_type(client, #pylint: disable=too-many-locals,invalid-name,too-many-arguments
                               external_provision=False,
                               no_wait=False,
                               application_type_build_path=None,
                               application_package_download_uri=None,
                               application_type_name=None,
                               application_type_version=None,
                               timeout=60):
    """Provisions or registers a Service Fabric application type with the
        cluster using the .sfpkg package in the external store or using the
        application package in the image store.
    """

    from azure.servicefabric.models.provision_application_type_description \
       import (ProvisionApplicationTypeDescription)
    from azure.servicefabric.models.external_store_provision_application_type_description \
        import (ExternalStoreProvisionApplicationTypeDescription)

    from azure.servicefabric.models.fabric_error import FabricErrorException

    provision_description = None

    # Validate inputs
    if external_provision:
        if application_type_build_path:
            raise CLIError(
                'application-type-build-path should not be specified for external provision.')

        if not all([application_package_download_uri, application_type_name,
                    application_type_version]):
            raise CLIError('Missing required parameters. The following are required: '
                           '--application-package-download-uri, --application-type-name, '
                           '--application-type-version.')
        provision_description = ExternalStoreProvisionApplicationTypeDescription(
            async_property=no_wait,
            application_package_download_uri=application_package_download_uri,
            application_type_name=application_type_name,
            application_type_version=application_type_version)
    else:
        if not application_type_build_path:
            raise CLIError('Missing required parameter '
                           '--application-type-build-path.')

        if any([application_package_download_uri, application_type_name,
                application_type_version]):
            raise CLIError('The following are should not be specified for image store provision: '
                           '--application-package-download-uri, --application-type-name, '
                           '--application-type-version.')

        provision_description = ProvisionApplicationTypeDescription(
            async_property=no_wait,
            application_type_build_path=application_type_build_path)

    api_version = "6.2"

    # Construct URLs
    url = '/ApplicationTypes/$/Provision'

    # Construct parameters
    query_parameters = {}
    query_parameters['api-version'] = client._serialize.query(
        "api_version", api_version, 'str')

    query_parameters['timeout'] = client._serialize.query(
        "timeout",
        timeout,
        'long',
        maximum=4294967295,
        minimum=1)

    # Construct headers
    header_parameters = {}
    header_parameters['Content-Type'] = 'application/json; charset=utf-8'

    # Construct body
    body_content = None
    if not external_provision:
        body_content = client._serialize.body(
            provision_description,
            'ProvisionApplicationTypeDescription')
    else:
        body_content = client._serialize.body(
            provision_description,
            'ExternalStoreProvisionApplicationTypeDescription')

    # Create a new sorted dictionary since we don't have move_to_end in python 2
    body_content_sorted = OrderedDict([('Kind', body_content['Kind'])])
    for key in body_content:
        if key != 'Kind':
            body_content_sorted[key] = body_content[key]

    if list(body_content_sorted.keys())[0] != "Kind":
        raise SFCTLInternalException(
            'provision_application_type: Kind must be the first item to be serialized.')

    # Construct and send request
    request = client._client.post(url, query_parameters)
    response = client._client.send(
        request, header_parameters, body_content_sorted)

    if response.status_code not in [200, 202]:
        raise FabricErrorException(client._deserialize, response)

    return None
