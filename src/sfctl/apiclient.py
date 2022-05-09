# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Azure Service Fabric API client factory"""

from knack.util import CLIError
from azure.servicefabric import ServiceFabricClientAPIs
from azure.core.credentials import TokenCredential
from azure.core.pipeline.policies import SansIOHTTPPolicy
from sfctl.auth import AdalAuthentication2
from sfctl.config import (security_type, ca_cert_info, cert_info,
                          client_endpoint, no_verify_setting)
class FakeAuthenticationPolicy(SansIOHTTPPolicy):
    """Fake authentication policy to avoid issues with token credentials being thrown in some scenaros"""

    def __init__(self):
        pass

class FakeCredentialProtocol(TokenCredential):
    """Fake credential used to pass in a credential for the API Client"""
    def __init__(self):
        pass

    def get_token(self, scopes):
        pass

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

    headers = {}

    if security_type() == 'aad':
        auth = AdalAuthentication2()
        headers['Authorization'] = auth.get_header()
    else:
        ca_cert = ca_cert_info()
        if ca_cert is not None:
            no_verify = ca_cert

    client = ServiceFabricClientAPIs(FakeCredentialProtocol(), endpoint=endpoint, retry_total=0,
                                     connection_verify=no_verify, enforce_https=False,
                                     connection_cert=cert_info(), authentication_policy=FakeAuthenticationPolicy())

    return client
