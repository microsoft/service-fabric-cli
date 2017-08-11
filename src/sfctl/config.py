# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Read and modify configuration settings related to the CLI"""

import os
import jsonpickle
from knack.config import CLIConfig

# Default names
SF_CLI_NAME = 'sfctl'
SF_CLI_CONFIG_DIR = os.path.join('~', '.{}'.format(SF_CLI_NAME))
SF_CLI_ENV_VAR_PREFIX = SF_CLI_NAME

def get_config_value(name, fallback=None):
    """Gets a config by name.

    In the case where the config name is not found, will use fallback value."""

    cli_config = CLIConfig(SF_CLI_CONFIG_DIR, SF_CLI_ENV_VAR_PREFIX)
    return cli_config.get('servicefabric', name, fallback)

def get_config_bool(name):
    """Checks if a config value is set to a valid bool value."""

    cli_config = CLIConfig(SF_CLI_CONFIG_DIR, SF_CLI_ENV_VAR_PREFIX)
    return cli_config.getboolean('servicefabric', name, False)

def set_config_value(name, value):
    """Set a config by name to a value."""

    cli_config = CLIConfig(SF_CLI_CONFIG_DIR, SF_CLI_ENV_VAR_PREFIX)
    cli_config.set_value('servicefabric', name, value)

def client_endpoint():
    """Cluster HTTP gateway endpoint address and port, represented as a URL."""

    return get_config_value('endpoint', None)

def security_type():
    """The selected security type of client."""

    return get_config_value('security', None)

def set_cluster_endpoint(endpoint):
    """Configure cluster endpoint"""
    set_config_value('endpoint', endpoint)

def no_verify_setting():
    """True to skip certificate SSL validation and verification"""

    return get_config_bool('no_verify')

def set_no_verify(no_verify):
    """Configure if cert verification should be skipped."""
    if no_verify:
        set_config_value('no_verify', 'true')
    else:
        set_config_value('no_verify', 'false')

def ca_cert_info():
    """CA certificate(s) path"""

    if get_config_bool('use_ca'):
        return get_config_value('ca_path', fallback=None)
    return None

def set_ca_cert(ca_path=None):
    """Configure paths to CA cert(s)."""
    if ca_path:
        set_config_value('ca_path', ca_path)
        set_config_value('use_ca', 'true')
    else:
        set_config_value('use_ca', 'false')

def cert_info():
    """Path to certificate related files, either a single file path or a
    tuple. In the case of no security, returns None."""

    sec_type = security_type()
    if sec_type == 'pem':
        return get_config_value('pem_path', fallback=None)
    if sec_type == 'cert':
        cert_path = get_config_value('cert_path', fallback=None)
        key_path = get_config_value('key_path', fallback=None)
        return cert_path, key_path

    return None

def aad_cache():
    """AAD token cache."""
    return jsonpickle.decode(get_config_value('aad_token', fallback=None)), \
           jsonpickle.decode(get_config_value('aad_cache', fallback=None))

def set_aad_cache(token, cache):
    """Set AAD token cache."""
    set_config_value('aad_token', jsonpickle.encode(token))
    set_config_value('aad_cache', jsonpickle.encode(cache))

def aad_metadata():
    """AAD metadata."""
    return get_config_value('authority_uri', fallback=None), \
           get_config_value('aad_resource', fallback=None), \
           get_config_value('aad_client', fallback=None)

def set_aad_metadata(uri, resource, client):
    """Set AAD metadata."""
    set_config_value('authority_uri', uri)
    set_config_value('aad_resource', resource)
    set_config_value('aad_client', client)

def set_auth(pem=None, cert=None, key=None, aad=False):
    """Set certificate usage paths"""

    if any([cert, key]) and pem:
        raise ValueError('Cannot specify both pem and cert or key')

    if any([cert, key]) and not all([cert, key]):
        raise ValueError('Must specify both cert and key')

    if pem:
        set_config_value('security', 'pem')
        set_config_value('pem_path', pem)
    elif cert or key:
        set_config_value('security', 'cert')
        set_config_value('cert_path', cert)
        set_config_value('key_path', key)
    elif aad:
        set_config_value('security', 'aad')
    else:
        set_config_value('security', 'none')
