# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Custom application type related commands"""

from knack.util import CLIError

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
        provision_description = {
            "Kind": "ExternalStore",
            "Async": no_wait,
            'ApplicationPackageDownloadUri': application_package_download_uri,
            'ApplicationTypeName': application_type_name,
            'ApplicationTypeVersion': application_type_version
        }
    else:
        if not application_type_build_path:
            raise CLIError('Missing required parameter '
                           '--application-type-build-path.')

        if any([application_package_download_uri, application_type_name,
                application_type_version]):
            raise CLIError('The following are should not be specified for image store provision: '
                           '--application-package-download-uri, --application-type-name, '
                           '--application-type-version.')

        provision_description = {
            "Kind": "ImageStorePath",
            'Async': no_wait,
            'ApplicationTypeBuildPath': application_type_build_path
        }

    return client.provision_application_type(provision_description)

