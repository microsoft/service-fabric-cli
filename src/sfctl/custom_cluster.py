# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Cluster level Service Fabric commands"""

from __future__ import print_function
from knack.util import CLIError
import adal
from datetime import datetime, timezone
import sfctl.config
from sfctl.config import client_endpoint, SF_CLI_VERSION_CHECK_INTERVAL
from azure.servicefabric.service_fabric_client_ap_is import ServiceFabricClientAPIs
from sfctl.state import get_sfctl_version
from sfctl.custom_exceptions import SFCTLInternalException
from knack.log import get_logger

logger = get_logger(__name__)

def select_arg_verify(endpoint, cert, key, pem, ca, aad, no_verify): #pylint: disable=invalid-name,too-many-arguments
    """Verify arguments for select command"""

    if not (endpoint.lower().startswith('http')
            or endpoint.lower().startswith('https')):
        raise CLIError('Endpoint must be HTTP or HTTPS')

    usage = ('Valid syntax : --endpoint [ [ --key --cert | --pem | --aad] '
             '[ --ca | --no-verify ] ]')

    if ca and not (pem or all([key, cert])):
        raise CLIError(usage)

    if no_verify and not (pem or all([key, cert]) or aad):
        raise CLIError(usage)

    if no_verify and ca:
        raise CLIError(usage)

    if any([cert, key]) and not all([cert, key]):
        raise CLIError(usage)

    if aad and any([pem, cert, key]):
        raise CLIError(usage)

    if pem and any([cert, key]):
        raise CLIError(usage)

def show_connection():
    """Show which Service Fabric cluster this sfctl instance is connected to."""
    endpoint = client_endpoint()

    if not endpoint:
        return None

    return endpoint

def get_rest_client(endpoint, cert=None, key=None, pem=None, ca=None, #pylint: disable=invalid-name, too-many-arguments
           aad=False, no_verify=False):

    from msrest import ServiceClient, Configuration
    from sfctl.auth import ClientCertAuthentication, AdalAuthentication
    from sfctl.config import set_aad_cache

    if aad:
        new_token, new_cache = get_aad_token(endpoint, no_verify)
        set_aad_cache(new_token, new_cache)
        return ServiceClient(AdalAuthentication(no_verify), Configuration(endpoint))

    else:
        client_cert = None
        if pem:
            client_cert = pem
        elif cert:
            client_cert = (cert, key)

        return ServiceClient(
            ClientCertAuthentication(client_cert, ca, no_verify),
            Configuration(endpoint)
        )


def select(endpoint, cert=None, key=None, pem=None, ca=None, #pylint: disable=invalid-name, too-many-arguments
           aad=False, no_verify=False):
    #pylint: disable-msg=too-many-locals
    """
    Connects to a Service Fabric cluster endpoint.
    If connecting to secure cluster, specify an absolute path to a cert (.crt)
    and key file (.key) or a single file with both (.pem). Do not specify both.
    Optionally, if connecting to a secure cluster, also specify an absolute
    path to a CA bundle file or directory of trusted CA certs. If using a
    directory of CA certs, `c_rehash <directory>` provided by OpenSSL must be run first to compute
    the certificate hashes and create the appropriate symbolics links.
    :param str endpoint: Cluster endpoint URL, including port and HTTP or HTTPS
    prefix
    :param str cert: Absolute path to a client certificate file
    :param str key: Absolute path to client certificate key file
    :param str pem: Absolute path to client certificate, as a .pem file
    :param str ca: Absolute path to CA certs directory to treat as valid
    or CA bundle
    file
    :param bool aad: Use Azure Active Directory for authentication
    :param bool no_verify: Disable verification for certificates when using
    HTTPS, note: this is an insecure option and should not be used for
    production environments
    """

    # Regarding c_rehash:
    # The c_rehash is needed when specifying a CA certs directory
    # because requests.Sessions which is used underneath requires
    # the c_rehash operation to be performed.
    # See http://docs.python-requests.org/en/master/user/advanced/

    from sfctl.config import (set_ca_cert, set_auth, set_aad_cache,
                              set_cluster_endpoint,
                              set_no_verify)

    select_arg_verify(endpoint, cert, key, pem, ca, aad, no_verify)

    # Make sure basic GET request succeeds
    rest_client = get_rest_client(endpoint, cert, key, pem, ca, aad, no_verify)
    rest_client.send(rest_client.get('/')).raise_for_status()

    set_cluster_endpoint(endpoint)
    set_no_verify(no_verify)
    set_ca_cert(ca)
    set_auth(pem, cert, key, aad)


def check_cluster_version(on_failure_or_connection, dummy_cluster_version = None):
    """ Check that the cluster version of sfctl is compatible with that of the cluster.

    Failures in making the API call (to check the cluster version)
    will be ignored and the time tracker
    will be reset to the current time. This is because we have no way of knowing if the
    API call failed because it doesn't exist on the cluster, or because of some other reason.
    We set the time tracker to the current time to avoid calling the API continuously
    for clusters without this API.

    Rather than each individual component deciding when to call this function, this should
    be called any time this might need to be triggered, and logic within this function will
    judge if a call to the cluster is required.

    :param on_failure_or_connection: True if this function is called due to an API call failure,
        or because it was called on connection to a new cluster endpoint.
        False otherwise.
    :type on_failure_or_connection: bool

    :param dummy_cluster_version: Used for testing purposes only. This is passed
        in to replace a call to the service fabric cluster to get the cluster version, in order to
        keep tests local.
    :type dummy_cluster_version: str

    :returns: True if versions match, or if the check is not performed. False otherwise.
    """

    from sfctl.state import get_cluster_version_check_time, set_cluster_version_check_time
    from warnings import warn

    # Before doing anything, see if a check needs to be triggered.
    if not on_failure_or_connection:  # always trigger version check if on failure or connection

        # Check if sufficient time has passed since last check
        last_check_time = get_cluster_version_check_time()
        if last_check_time is not None:
            # If we've already checked the cluster version before, see how long ago it has been
            time_since_last_check = datetime.now(timezone.utc) - last_check_time
            allowable_time = datetime.timedelta(hours=SF_CLI_VERSION_CHECK_INTERVAL)
            if allowable_time > time_since_last_check:
                # Don't perform any checks
                return True

    rest_client = get_rest_client(sfctl.config.get_cluster_auth())

    auth = rest_client.creds

    client = ServiceFabricClientAPIs(auth, base_url=sfctl.config.client_endpoint())

    sfctl_version = get_sfctl_version()
    cluster_version = None

    # Update the timestamp of the last cluster version check
    set_cluster_version_check_time()

    if dummy_cluster_version is None:
        # This command may fail for various reasons. Most common reason as of writing this comment
        # is that the corresponding get_cluster_version API on the cluster doesn't exist.
        try:
            cluster_version = client.get_cluster_version().Version
        except Exception as ex:
            logger.info('Check cluster version failed due to error: %s', str(ex))
            return True
    else:
        cluster_version = dummy_cluster_version

    if cluster_version is None:
        # Do no checks if the get cluster version API fails, since most likely it failed
        # because the API doesn't exist.
        return True

    elif not sfctl_cluster_version_matches(cluster_version, sfctl_version):
        warn(str.format(
            'CLI sfctl has version "{0}" which does not match the cluster version "{1}". '
            'See https://docs.microsoft.com/azure/service-fabric/service-fabric-cli#service-fabric-target-runtime '
            'for version compatibility. Upgrade to a compatible version for the best experience.',
        sfctl_version,
        cluster_version))
        return False

    return True


def sfctl_cluster_version_matches(cluster_version, sfctl_version):
    """
    Check if the sfctl version and the cluster version is compatible with each other.
    :param cluster_version: str representing the cluster runtime version of the connected cluster
    :param sfctl_version: str representing this sfctl distribution version
    :return: True if they are a match. False otherwise.
    """

    if sfctl_version == '7.0.0':

        return True if cluster_version.startswith('6.4') else False

    # If we forget to update this code before a new release, the tests which call this method
    # will fail.
    raise SFCTLInternalException(str.format(
        'Invalid sfctl version {0} provided for check against cluster version {1}.',
        sfctl_version,
        cluster_version))


def get_aad_token(endpoint, no_verify):
    #pylint: disable-msg=too-many-locals
    """Get AAD token"""

    from sfctl.auth import ClientCertAuthentication
    from sfctl.config import set_aad_metadata

    auth = ClientCertAuthentication(None, None, no_verify)

    client = ServiceFabricClientAPIs(auth, base_url=endpoint)
    aad_metadata = client.get_aad_metadata()

    if aad_metadata.type != "aad":
        raise CLIError("Not AAD cluster")

    aad_resource = aad_metadata.metadata

    tenant_id = aad_resource.tenant
    authority_uri = aad_resource.login + '/' + tenant_id
    context = adal.AuthenticationContext(authority_uri,
                                         api_version=None)
    cluster_id = aad_resource.cluster
    client_id = aad_resource.client

    set_aad_metadata(authority_uri, cluster_id, client_id)

    code = context.acquire_user_code(cluster_id, client_id)
    print(code['message'])
    token = context.acquire_token_with_device_code(
        cluster_id, code, client_id)
    print("Succeed!")
    return token, context.cache
