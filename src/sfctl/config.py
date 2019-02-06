# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Read and modify configuration settings related to the CLI"""

import os
import json
from knack.config import CLIConfig
from knack import CLI
from adal.token_cache import TokenCache

# Default names
SF_CLI_NAME = 'sfctl'
SF_CLI_CONFIG_DIR = os.path.expanduser(os.path.join('~', '.{0}'.format(SF_CLI_NAME)))
SF_CLI_ENV_VAR_PREFIX = SF_CLI_NAME

# How often to check sfctl version and cluster version for compatibility with each other (in hours).
SF_CLI_VERSION_CHECK_INTERVAL = 24


def get_config_value(name, fallback=None):
    """Gets a config by name.

    In the case where the config name is not found, will use fallback value."""

    cli_config = CLIConfig(SF_CLI_CONFIG_DIR, SF_CLI_ENV_VAR_PREFIX)

    return cli_config.get('servicefabric', name, fallback)


def get_config_bool(name, fallback=False):
    """Checks if a config value is set to a valid bool value."""

    cli_config = CLIConfig(SF_CLI_CONFIG_DIR, SF_CLI_ENV_VAR_PREFIX)
    return cli_config.getboolean('servicefabric', name, fallback)


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
    token_cache = TokenCache()
    token_cache.deserialize(get_config_value('aad_cache', fallback=None))
    return json.loads(get_config_value('aad_token', fallback=None)), token_cache


def set_aad_cache(token, cache):
    """
    Set AAD token cache.
    :param token: dict with several keys, include "accessToken" and "refreshToken"
    :param cache: adal.token_cache.TokenCache
    :return: None
    """

    set_config_value('aad_token', json.dumps(token))
    set_config_value('aad_cache', cache.serialize())

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


def using_aad():
    """
    :return: True if security type is 'aad'. False otherwise
    """
    return security_type() == 'aad'


def get_cluster_auth():
    """
    Return the information that was added to config file by the function select cluster.

    :return: a dictionary with keys: endpoint, cert, key, pem, ca, aad, no_verify
    """

    cluster_auth = dict()
    cluster_auth['endpoint'] = client_endpoint()
    cluster_auth['cert'] = get_config_value('cert_path')
    cluster_auth['key'] = get_config_value('key_path')
    cluster_auth['pem'] = get_config_value('pem_path')
    cluster_auth['ca'] = ca_cert_info()
    cluster_auth['aad'] = using_aad()
    cluster_auth['no_verify'] = no_verify_setting()

    return cluster_auth


def set_telemetry_config(telemetry_on):
    """
    Sets whether or not telemetry is turned on in the configuration file.
    :param telemetry_on: bool. True means telemetry should be on.
    :return: None
    """
    if telemetry_on:
        set_config_value('use_telemetry', 'true')
    else:
        set_config_value('use_telemetry', 'false')


def get_telemetry_config():
    """
    Gets whether or not telemetry is turned on
    Returns True if no value is set.
    :return: bool. True if telemetry is on. False otherwise.
    """
    return get_config_bool('use_telemetry', fallback=True)


def get_cli_version_from_pkg():
    """
    Reads and returns the version number of sfctl. This is the version sfctl is released with.
    For example, 6.0.0.
    :return: str
    """
    from pkg_resources import get_distribution

    pkg = get_distribution("sfctl")
    sfctl_version = pkg.version
    return '{0}'.format(sfctl_version)


class VersionedCLI(CLI):
    """Extend CLI to override get_cli_version."""
    def get_cli_version(self):
        return get_cli_version_from_pkg()
