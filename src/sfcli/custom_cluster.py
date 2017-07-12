def sf_select_verify(endpoint, cert, key, pem, ca, no_verify):
    if not (endpoint.lower().startswith("http") or endpoint.lower().startswith("https")):
        raise CLIError("Endpoint must be HTTP or HTTPS")

    usage = "Valid syntax : --endpoint [ [ --key --cert | --pem ] [ --ca | --no-verify ] ]"

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

def sf_select(endpoint, cert=None,
              key=None, pem=None, ca=None, no_verify=False):
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
    from azure.cli.core._config import set_global_config_value

    sf_select_verify(endpoint, cert, key, pem, ca, no_verify)

    if pem:
        set_global_config_value("servicefabric", "pem_path", pem)
        set_global_config_value("servicefabric", "security", "pem")
    elif cert:
        set_global_config_value("servicefabric", "cert_path", cert)
        set_global_config_value("servicefabric", "key_path", key)
        set_global_config_value("servicefabric", "security", "cert")
    else:
        set_global_config_value("servicefabric", "security", "none")

    if ca:
        set_global_config_value("servicefabric", "use_ca", "True")
        set_global_config_value("servicefabric", "ca_path", ca)
    else:
        set_global_config_value("servicefabric", "use_ca", "False")

    if no_verify:
        set_global_config_value("servicefabric", "no_verify", "True")
    else:
        set_global_config_value("servicefabric", "no_verify", "False")

    set_global_config_value("servicefabric", "endpoint", endpoint)