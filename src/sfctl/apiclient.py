# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Azure Service Fabric API client factory"""

from knack.util import CLIError
from azure.servicefabric import ServiceFabricClientAPIs
from azure.core.credentials import TokenCredential

from sfctl.auth import (ClientCertAuthentication, AdalAuthentication)
from sfctl.config import (security_type, ca_cert_info, cert_info,
                          client_endpoint, no_verify_setting)

class dummmy_protocol(TokenCredential):
    def __init__(self):
        self


def create(_):
    """Create a client for Service Fabric APIs."""

    endpoint = client_endpoint()

    if not endpoint:
        raise CLIError('Connection endpoint not found. '
                       'Before running sfctl commands, connect to a cluster using '
                       'the "sfctl cluster select" command. '
                       'If you are seeing this message on Linux after already selecting a cluster, '
                       'you may need to run the command with sudo.')

    no_verify = no_verify_setting()

    if security_type() == 'aad':
        auth = AdalAuthentication(no_verify)
    else:
        ca_cert = ca_cert_info()
        if ca_cert is not None:
            no_verify = ca_cert
    
    dummy_credential = dummmy_protocol()

    client = ServiceFabricClientAPIs(dummy_credential, base_url=endpoint, retry_total=0, connection_verify=no_verify, connection_cert=cert_info())

    return client
