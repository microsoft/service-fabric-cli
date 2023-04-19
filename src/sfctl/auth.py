# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Client certificate authentication for Service Fabric API clients"""

import adal
from azure.core.credentials import TokenCredential
from azure.core.pipeline.policies import SansIOHTTPPolicy


def get_aad_header():
    """Create requests session with AAD auth headers

    :rtype: requests.Session.
    """

    from sfctl.config import (aad_metadata, aad_cache)

    authority_uri, cluster_id, client_id = aad_metadata()
    existing_token, existing_cache = aad_cache()
    context = adal.AuthenticationContext(authority_uri,
                                            cache=existing_cache)
    new_token = context.acquire_token(cluster_id,
                                        existing_token['userId'], client_id)
    header = "{} {}".format("Bearer", new_token['accessToken'])

    return header

class AuthenticationPolicy(SansIOHTTPPolicy):
    """Authentication policy to avoid issues with token credentials being thrown in some scenarios"""

    def __init__(self):
        pass

class CredentialProtocol(TokenCredential): # pylint: disable=R0903
    """Credential used to pass in a credential for the API Client"""
    def __init__(self): # pylint: disable=super-init-not-called
        pass

    def get_token(self, *scopes, claims, tenant_id, **kwargs):
        pass
