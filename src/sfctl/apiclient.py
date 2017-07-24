# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Azure Service Fabric API client factory"""

from knack.util import CLIError
from azure.servicefabric.service_fabric_client_ap_is import (
    ServiceFabricClientAPIs
)
from sfctl.auth import ClientCertAuthentication
from sfctl.config import (ca_cert_info, cert_info, client_endpoint,
                          no_verify_setting)

def create(_):
    """Create a client for Service Fabric APIs."""

    cert = cert_info()
    ca_cert = ca_cert_info()
    no_verify = no_verify_setting()
    endpoint = client_endpoint()

    if not endpoint:
        raise CLIError("Connection endpoint not found")

    auth = ClientCertAuthentication(cert, ca_cert, no_verify)
    return ServiceFabricClientAPIs(auth, base_url=endpoint)
