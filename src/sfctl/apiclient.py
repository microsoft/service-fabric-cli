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
from sfctl.auth import (ClientCertAuthentication, AdalAuthentication)
from sfctl.config import (security_type, ca_cert_info, cert_info,
                          client_endpoint, no_verify_setting)

def create(_):
    """Create a client for Service Fabric APIs."""

    endpoint = client_endpoint()

    if not endpoint:
        raise CLIError("Connection endpoint not found. "
                       "Before running sfctl commands, connect to a cluster using "
                       "the 'sfctl cluster select' command.")

    no_verify = no_verify_setting()

    if security_type() == 'aad':
        auth = AdalAuthentication(no_verify)
    else:
        cert = cert_info()
        ca_cert = ca_cert_info()
        auth = ClientCertAuthentication(cert, ca_cert, no_verify)

    return ServiceFabricClientAPIs(auth, base_url=endpoint)
