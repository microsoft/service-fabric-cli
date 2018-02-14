# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Help documentation for Service Fabric application and compose commands."""

from knack.help_files import helps

# the pipe in long-summary preserves the newlines.
helps['application provision'] = """
    type: command
    short-summary: Provisions or registers a Service Fabric application type with the
        cluster using the .sfpkg package in the
        external store or using the application package in the image store.
    long-summary:
        Provisions a Service Fabric application type with the cluster.
        This is required before any new applications can be instantiated.
        The provision operation can be performed either on the application package specified
        by the relativePathInImageStore, or by using the URI of the external .sfpkg.
        Unless --external-provision is set, this command will expect image store provision.
    parameters:
        - name: --external-provision
          type: string
          short-summary: The location from where application package can be registered or
            provisioned. Indicates that the provision is for an application package that was
            previously uploaded to an external store. The application package ends with
            the extension *.sfpkg.
        - name: --application-type-build-path
          type: string
          short-summary: For provision kind image store only. The relative path for the
            application package in the image store specified during the prior upload operation.
        - name: --application-package-download-uri
          type: string
          short-summary: The path to the '.sfpkg' application package from where the application
            package can be downloaded using HTTP or HTTPS protocols.
          long-summary: For provision kind external store only. The application package can be
            stored in an external store that provides GET operation to download the file.
            Supported protocols are HTTP and HTTPS, and the path must allow READ access.
        - name: --application-type-name
          type: string
          short-summary: For provision kind external store only. The application type name
            represents the name of the application type found in the application manifest.
        - name: --application-type-version
          type: string
          short-summary: For provision kind external store only. The application type version
            represents the version of the application type found in the application manifest.
        - name: --no-wait
          type: bool
          short-summary: Indicates whether or not provisioning should occur asynchronously.
          long-summary: When set to true, the provision operation returns when the request is
            accepted by the system, and the
            provision operation continues without any timeout limit. The default value is false.
            For large application packages, we recommend setting the value to true.
"""
