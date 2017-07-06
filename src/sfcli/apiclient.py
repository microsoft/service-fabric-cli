"""Azure Service Fabric API client factory"""

from knack.config import CLIConfig
from knack.util import CLIError
from azure.servicefabric.service_fabric_client_ap_is import (
    ServiceFabricClientAPIs
)
from sf_cli.auth import ClientCertAuthentication

class SFApiClient(object):
    """Configure and generate a Service Fabric client for interacting with
    a cluster through an HTTP gateway"""

    def __init__(self, config_dir, env_var_prefix):
        self.cli_config = CLIConfig(config_dir=config_dir,
                                    config_env_var_prefix=env_var_prefix)

    def client_endpoint(self):
        """Cluster HTTP gateway endpoint address and port, represented as a
        URL."""

        return self.cli_config.get('connection', 'endpoint', None)

    def no_verify_setting(self):
        """True to skip certificate SSL validation and verification"""

        return self.cli_config.get('servicefabric',
                                   'no_verify', fallback=False) == 'True'

    def ca_cert_info(self):
        """CA certificate(s) path"""

        using_ca = self.cli_config.get('servicefabric',
                                       'use_ca', fallback=False)
        if using_ca == 'True':
            return self.cli_config.get('servicefabric',
                                       'ca_path', fallback=None)
        return None

    def cert_info(self):
        """Path to certificate related files, either a single file path or a
        tuple. In the case of no security, returns None."""

        security_type = str(self.cli_config.get('servicefabric',
                                                'security', fallback=''))
        if security_type == 'pem':
            return self.cli_config.get('servicefabric',
                                       'pem_path', fallback=None)
        if security_type == 'cert':
            cert_path = self.cli_config.get('servicefabric',
                                            'cert_path', fallback=None)
            key_path = self.cli_config.get('servicefabric',
                                           'key_path', fallback=None)
            return cert_path, key_path

        return None

    def client(self):
        """Returns a function that when called will generate a client for the
        Service Fabric APIs."""

        cert = self.cert_info()
        ca_cert = self.ca_cert_info()
        no_verify = self.no_verify_setting()
        endpoint = self.client_endpoint()

        def client_fcn(_):
            """Configure and return a Service Fabric API client"""

            if not endpoint:
                raise CLIError("Connection endpoint not found")

            auth = ClientCertAuthentication(cert, ca_cert, no_verify)
            return ServiceFabricClientAPIs(auth, base_url=endpoint)

        return client_fcn
