# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Azure Service Fabric API client factory"""

from knack.util import CLIError
from azure.servicefabric import ServiceFabricClientAPIs

from sfctl.auth import (ClientCertAuthentication, AdalAuthentication)
from sfctl.config import (security_type, ca_cert_info, cert_info,
                          client_endpoint, no_verify_setting)

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
        cert = cert_info()
        ca_cert = ca_cert_info()
        auth = ClientCertAuthentication(cert, ca_cert, no_verify)

    client = ServiceFabricClientAPIs(auth, base_url=endpoint)

    # client.config.retry_policy has type msrest.pipeline.ClientRetryPolicy
    client._config.retry_policy.total = False
    client._config.retry_policy.policy.total = False

    # msrest defines ClientRetryPolicy in pipline.py.
    # ClientRetryPolicy.__init__ defines values for status_forcelist
    # which is passed to urllib3.util.retry.Retry
    client._config.retry_policy.policy.status_forcelist = None

    return client


def mesh_code_package_create(_):
    """Create a client for mesh code package APIs."""
    client = create(_)
    return client.mesh_code_package

def mesh_gateway_create(_):
    """Create a client for mesh gateway APIs."""
    client = create(_)
    return client.mesh_gateway

def mesh_secret_create(_):
    """Create a client for mesh secret APIs."""
    client = create(_)
    return client.mesh_secret

def mesh_secret_value_create(_):
    """Create a client for mesh secret value APIs."""
    client = create(_)
    return client.mesh_secret_value

def mesh_network_create(_):
    """Create a client for mesh network APIs."""
    client = create(_)
    return client.mesh_network

def mesh_app_create(_):
    """Create a client for mesh application APIs."""
    client = create(_)
    return client.mesh_application

def mesh_volume_create(_):
    """Create a client for mesh volume APIs."""
    client = create(_)
    return client.mesh_volume

def mesh_service_create(_):
    """Create a client for mesh service APIs."""
    client = create(_)
    return client.mesh_service

def mesh_service_replica_create(_):
    """Create a client for mesh service-replica APIs."""
    client = create(_)
    return client.mesh_service_replica
