# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Cluster level Service Fabric commands"""

from knack.util import CLIError

def select_arg_verify(endpoint, cert, key, pem, ca, no_verify):
    """Verify arguments for select command"""

    if not (endpoint.lower().startswith('http')
            or endpoint.lower().startswith('https')):
        raise CLIError('Endpoint must be HTTP or HTTPS')

    usage = ('Valid syntax : --endpoint [ [ --key --cert | --pem ] '
             '[ --ca | --no-verify ] ]')

    if ca and not (pem or all([key, cert])):
        raise CLIError(usage)

    if no_verify and not (pem or all([key, cert])):
        raise CLIError(usage)

    if no_verify and ca:
        raise CLIError(usage)

    if any([cert, key]) and not all([cert, key]):
        raise CLIError(usage)

    if pem and any([cert, key]):
        raise CLIError(usage)

def select(endpoint, cert=None, key=None, pem=None, ca=None, no_verify=False):
    """
    Connects to a Service Fabric cluster endpoint.
    If connecting to secure cluster specify a cert (.crt) and key file (.key)
    or a single file with both (.pem). Do not specify both. Optionally, if
    connecting to a secure cluster, specify also a path to a CA bundle file
    or directory of trusted CA certs.
    :param str endpoint: Cluster endpoint URL, including port and HTTP or HTTPS
    prefix
    :param str cert: Path to a client certificate file
    :param str key: Path to client certificate key file
    :param str pem: Path to client certificate, as a .pem file
    :param str ca: Path to CA certs directory to treat as valid or CA bundle
    file
    :param bool no_verify: Disable verification for certificates when using
    HTTPS, note: this is an insecure option and should not be used for
    production environments
    """
    from sfctl.config import (set_ca_cert, set_cert, set_cluster_endpoint,
                              set_no_verify)
    from msrest import ServiceClient, Configuration
    from sfctl.auth import ClientCertAuthentication

    select_arg_verify(endpoint, cert, key, pem, ca, no_verify)

    client_cert = None
    if pem:
        client_cert = pem
    elif cert:
        client_cert = (cert, key)

    rest_client = ServiceClient(
        ClientCertAuthentication(client_cert, ca, no_verify),
        Configuration(endpoint)
    )

    # Make sure basic GET request succeeds
    rest_client.send(rest_client.get('/')).raise_for_status()

    set_ca_cert(ca)
    set_cert(pem, cert, key)
    set_no_verify(no_verify)
    set_cluster_endpoint(endpoint)
