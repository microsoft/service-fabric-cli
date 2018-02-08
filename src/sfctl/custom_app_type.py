# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Custom application type related commands"""

from knack.util import CLIError

def provision_application_type( #pylint: disable=invalid-name,missing-docstring,too-many-arguments
        client,
        no_wait=False,
        external=False,
        application_type_build_path=None,
        application_package_download_uri=None,
        application_type_name=None,
        application_type_version=None,
        timeout=60
    ):
    from azure.servicefabric.models.provision_application_type_description import (
        ProvisionApplicationTypeDescription
    )
    from azure.servicefabric.models.external_store_provision_application_type_description import (
        ExternalStoreProvisionApplicationTypeDescription
    )

    if external and not all([application_package_download_uri,
                             application_type_name,
                             application_type_version]):
        raise CLIError("Must specify download uri, type name and type version")

    if external and application_type_build_path:
        raise CLIError("Cannot specify a build path and external")

    if not external and not application_type_build_path:
        raise CLIError("Must specify an application type build path")

    if not external and any([application_package_download_uri,
                             application_type_name,
                             application_type_version]):
        raise CLIError("Cannot specify the name, version, nor download uri and external")

    provision_desc = None
    if external:
        provision_desc = ExternalStoreProvisionApplicationTypeDescription(
            no_wait,
            application_type_name=application_type_name,
            application_package_download_uri=application_package_download_uri,
            application_type_version=application_type_version
        )
    else:
        provision_desc = ProvisionApplicationTypeDescription(
            no_wait,
            application_type_build_path=application_type_build_path
        )

    client.provision_application_type(provision_desc, timeout)
