# Service Fabric Cross Platform Command-line Interface

Command-line interface(CLI) for interacting with Azure Service Fabric clusters and their related entities.

## Compatibility between sfctl and Service Fabric versions
sfctl is forward compatible with newer versions of Service Fabric runtime i.e. an older version of sfctl can work with newer versions of Service Fabric runtime but will not support new commands available in later versions. This also means that newer versions of sfctl will not be able to communicate with older versions of Service Fabric.

Following table gives the mapping of sfctl versions and Service Fabric runtime versions.
<table>
<thead>
<tr>
<th>sfctl version</th><th>Service Fabric runtime version</th>
</tr>
</thead>
<tr><td>1.1.0</td><td>5.6.130 or later</td></tr>
<tr><td>2.0.0</td><td>6.0 and later</td></tr>
</table>
	
## Installing sfctl using pip

#### Perquisite
[Python 3.6](https://www.python.org/) or later installed on the machine.

pip commands to Install, Upgrade and Uninstall to a central location on the machine require running commands from an admin Command prompt (Windows) or a Terminal window with sudo access (Linux or Mac). On Linux or Mac, prepend sudo to each of these commands below.

#### Install latest version
```
pip3 install sfctl
```
#### Install a specific version
Identify the the most appropriate version from table above and specify it in the following command
```
pip3 install sfctl==replace-with-required-version
```
Following will install version 1.1.0 of sfctl
```
pip3 install sfctl==1.1.0
```
#### Determine version of sfctl installed on the machine
```
pip3 show sfctl
```
#### Upgrade to latest version
```
pip3 install -U sfctl
```
#### Upgrade to specific version
```
pip3 install -U sfctl==replace-with-required-version
```
#### Uninstall
```
pip uninstall -y sfctl
```
## Installing multiple versions side-by-side using python virtual environment
There may be a need to install different versions of sfctl side by side to interact with clusters running different versions of Service Fabric runtime. 

[pipenv](https://docs.pipenv.org/) package can be used to setup a python virtual environment that can be used to install a different version of sfctl separate from the globally installed version.

1. Install pipenv.

    **NOTE:** Only this command requires an admin command prompt or sudo access. Do not use admin command prompt or sudo for rest of the commands below
    ```
    pip3 install pipenv
    ```
2. Create a directory for installing files for virtual environment (commands below installs sfctl 1.1.0)
    ```
    mkdir sfctl-1.1.0
    ```
3. Install sfctl in virtual env
    ```
    pipenv --three install sfctl-1.1.0
    ```
4. Create a shell that uses files in virtual environment
    ```
    pipenv --three shell
    ```
5. Run 1.1.0 of sfctl
    ```
    pip show sfctl
    sfctl --help
    ```
6. Exit virtual environment shell
    ```
    exit
    ```
7. Run globally installed version of sfctl
    ```
    pip show sfctl
    sfctl --help
    ```

## Installing multiple versions side-by-side in a Docker container
sfctl github repo has Dockerfile to generate a container with the required version of sfctl.

1. Install [Docker CE](https://www.docker.com/community-edition) the machine. 

2. Clone [sfctl repo](https://github.com/Azure/service-fabric-cli) using information on the github page - https://github.com/Azure/service-fabric-cli

2. Open a Command Prompt (Windows) or Terminal window (Linux or Mac) and navigate to the Dockerfiles folder under the root of the enlistment

    ```
    pushd path-to-root-of-enlistment/Dockerfiles
    ```

3. Build the docker image

    Windows
    ```
    REM replace 2.0.0 with required version
    docker build -t sfctl_2.0.0 -f Dockerfile.windows --build-arg sfctl_version=2.0.0 .
    ```
    Linux
    ```
    # replace 2.0.0 with required version
    docker build -t sfctl_2.0.0 -f Dockerfile.linux --build-arg sfctl_version=2.0.0 .
    ```

4. Start the container in interactive mode. Replace the name of the name of the image with the image for the require version
    ```
    docker run -it sfctl_2.0.0
    ```
5. Once the container starts at the container command prompt run sfctl
    ```
    sfctl -h
    ...
    ```
6. Exit the container
    ```
    exit
    ```
## Command line options and commands
 sfctl has extensive help for command line options and commands. --help option gives detailed information

Output from sfctl 2.0.0
```
sfctl --help

Group
    sfctl : Commands for managing Service Fabric clusters and entities. This version is compatible
    with Service Fabric 6.0 runtime.
        Commands follow the noun-verb pattern. See subgroups for more information.

Subgroups:
    application: Create, delete, and manage applications and application types.
    chaos      : Start, stop and report on the chaos test service.
    cluster    : Select, manage and operate Service Fabric clusters.
    compose    : Create, delete and manage Docker Compose applications.
    is         : Query and send commands to the infrastructure service.
    node       : Manage the nodes that form a cluster.
    partition  : Query and manage partitions for any service.
    replica    : Manage the replicas that belong to service partitions.
    rpm        : Query and send commands to the repair manager service.
    sa-cluster : Manage stand-alone Service Fabric clusters.
    service    : Create, delete and manage service, service types and service packages.
    store      : Perform basic file level operations on the cluster image store.



sfctl cluster select --help

Command
    sfctl cluster select: Connects to a Service Fabric cluster endpoint.
        If connecting to secure cluster specify a cert (.crt) and key file (.key) or a single file
        with both (.pem). Do not specify both. Optionally, if connecting to a secure cluster,
        specify also a path to a CA bundle file or directory of trusted CA certs.

Arguments
    --endpoint [Required]: Cluster endpoint URL, including port and HTTP or HTTPS prefix.
    --aad                : Use Azure Active Directory for authentication.
    --ca                 : Path to CA certs directory to treat as valid or CA bundle file.
    --cert               : Path to a client certificate file.
    --key                : Path to client certificate key file.
    --no-verify          : Disable verification for certificates when using HTTPS, note: this is an
                           insecure option and should not be used for production environments.
    --pem                : Path to client certificate, as a .pem file.

Global Arguments
    --debug              : Increase logging verbosity to show all debug logs.
    --help -h            : Show this help message and exit.
    --output -o          : Output format.  Allowed values: json, jsonc, table, tsv.  Default: json.
    --query              : JMESPath query string. See http://jmespath.org/ for more information and
                           examples.
    --verbose            : Increase logging verbosity. Use --debug for full debug logs.
```


## Developer Help and Documentation

See the
[corresponding Wiki](https://github.com/Azure/service-fabric-cli/wiki) for
more information.

## Contributing

This project has adopted the
[Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information, see the
[Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any
additional questions or comments.
