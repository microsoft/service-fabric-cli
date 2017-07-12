def sf_create_compose_application(client, compose_file, application_id, repo_user=None, encrypted=False,
                                  repo_pass=None, timeout=60):
    # We need to read from a file which makes this a custom command
    # Encrypted param to indicate a password will be prompted
    """
    Creates a Service Fabric application from a Compose file
    :param str application_id:  The id of application to create from
    Compose file. This is typically the full id of the application
    including "fabric:" URI scheme
    :param str compose_file: Path to the Compose file to use
    :param str repo_user: Container repository user name if needed for
    authentication
    :param bool encrypted: If true, indicate to use an encrypted password
    rather than prompting for a plaintext one
    :param str repo_pass: Encrypted container repository password
    """
    from azure.cli.core.util import read_file_content
    from azure.cli.core.prompting import prompt_pass
    # pylint: disable=line-too-long
    from azure.servicefabric.models.create_compose_application_description import CreateComposeApplicationDescription
    from azure.servicefabric.models.repository_credential import RepositoryCredential

    if (any([encrypted, repo_pass]) and
            not all([encrypted, repo_pass, repo_user])):
        raise CLIError(
            "Invalid arguments: [ --application_id --file | "
            "--application_id --file --repo_user | --application_id --file "
            "--repo_user --encrypted --repo_pass ])"
        )

    if repo_user:
        plaintext_pass = prompt_pass("Container repository password: ", False,
                                     "Password for container repository "
                                     "containing container images")
        repo_pass = plaintext_pass

    repo_cred = RepositoryCredential(repo_user, repo_pass, encrypted)

    file_contents = read_file_content(compose_file)

    model = CreateComposeApplicationDescription(application_id, file_contents,
                                                repo_cred)

    client.create_compose_application(model, timeout)


def validate_app_path(app_path):
    abspath = os.path.abspath(app_path)
    if os.path.isdir(abspath):
        return abspath
    else:
        raise ValueError("Invalid path to application directory: {0}".format(abspath))


def sf_upload_app(path, show_progress=False):  # pylint: disable=too-many-locals
    """
    Copies a Service Fabric application package to the image store.
    The cmdlet copies a Service Fabric application package to the image store.
    After copying the application package, use the sf application provision
    cmdlet to register the application type.
    Can optionally display upload progress for each file in the package.
    Upload progress is sent to `stderr`.
    :param str path: The path to your local application package
    :param bool show_progress: Show file upload progress
    """
    from azure.cli.command_modules.sf.config import SfConfigParser

    abspath = validate_app_path(path)
    basename = os.path.basename(abspath)

    sf_config = SfConfigParser()
    endpoint = sf_config.connection_endpoint()
    cert = sf_config.cert_info()
    ca_cert = False
    if cert is not None:
        ca_cert = sf_config.ca_cert_info()
    total_files_count = 0
    current_files_count = 0
    total_files_size = 0
    # For py2 we use dictionary instead of nonlocal
    current_files_size = {"size": 0}

    for root, _, files in os.walk(abspath):
        total_files_count += (len(files) + 1)
        for f in files:
            t = os.stat(os.path.join(root, f))
            total_files_size += t.st_size

    def print_progress(size, rel_file_path):
        current_files_size["size"] += size
        if show_progress:
            print(
                "[{}/{}] files, [{}/{}] bytes, {}".format(
                    current_files_count,
                    total_files_count,
                    current_files_size["size"],
                    total_files_size,
                    rel_file_path), file=sys.stderr)

    for root, _, files in os.walk(abspath):
        rel_path = os.path.normpath(os.path.relpath(root, abspath))
        for f in files:
            url_path = (
                os.path.normpath(os.path.join("ImageStore", basename,
                                              rel_path, f))
            ).replace("\\", "/")
            fp = os.path.normpath(os.path.join(root, f))
            with open(fp, 'rb') as file_opened:
                url_parsed = list(urlparse(endpoint))
                url_parsed[2] = url_path
                url_parsed[4] = urlencode(
                    {"api-version": "3.0-preview"})
                url = urlunparse(url_parsed)

                def file_chunk(target_file, rel_path, print_progress):
                    chunk = True
                    while chunk:
                        chunk = target_file.read(100000)
                        print_progress(len(chunk), rel_path)
                        yield chunk

                fc = file_chunk(file_opened, os.path.normpath(
                    os.path.join(rel_path, f)
                ), print_progress)
                requests.put(url, data=fc, cert=cert,
                             verify=ca_cert)
                current_files_count += 1
                print_progress(0, os.path.normpath(
                    os.path.join(rel_path, f)
                ))
        url_path = (
            os.path.normpath(os.path.join("ImageStore", basename,
                                          rel_path, "_.dir"))
        ).replace("\\", "/")
        url_parsed = list(urlparse(endpoint))
        url_parsed[2] = url_path
        url_parsed[4] = urlencode({"api-version": "3.0-preview"})
        url = urlunparse(url_parsed)
        requests.put(url, cert=cert, verify=ca_cert)
        current_files_count += 1
        print_progress(0, os.path.normpath(os.path.join(rel_path, '_.dir')))

    if show_progress:
        print("[{}/{}] files, [{}/{}] bytes sent".format(
            current_files_count,
            total_files_count,
            current_files_size["size"],
            total_files_size), file=sys.stderr)

