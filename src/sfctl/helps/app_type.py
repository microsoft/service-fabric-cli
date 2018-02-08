# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Help documentation for Service Fabric application and compose commands."""

from knack.help_files import helps

helps['application provision'] = """
    type: command
    short-summary: Provisions or registers a Service Fabric application type with the cluster.
    long-summary: Provisions a Service Fabric application type with the cluster. This is required
      before any new applications can be instantiated. The provision operation can be performed
      either on the application package specified by the relativePathInImageStore, or by using the
      URI of the external .sfpkg.
    parameters:
        - name: --no-wait
          type: bool
          short-summary: Indicates the provision operation should return when the request is
            accepted by the system, and the provision operation continues without any timeout
            limit.
        - name: --external
          type: bool
          short-summary: Indicates the provision should be performed from an external package
            source.
        - name: --application-type-build-path
          type: string
          short-summary: The relative path for the application package in the image store specified
            during the prior upload operation. Only applies if external is not specified.
        - name: --application-package-download-uri
          type: string
          short-summary: The path to the .sfpkg application package from where the application
            package can be downloaded using HTTP or HTTPS protocols. The application package can be
            stored in an external store that provides GET operation to download the file. Supported
            protocols are HTTP and HTTPS, and the path must allow READ access. Only applies if
            external is specified.
        - name: --application-type-name
          type: string
          short-summary: The application type name represents the name of the application type
            found in the application manifest. Only applies if external is specified.
        - name: --application-type-version
          type: string
          short-summary: The application type version represents the version of the application
            type found in the application manifest. Only applies if external is specified.
"""
