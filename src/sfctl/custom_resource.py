# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Commands related to managing Service Fabric Mesh resources"""

from knack.util import CLIError
import json
import enum
from collections import OrderedDict
class ResourceType(enum.Enum):
    """ Defines the valid yaml resource types
        which are parseable by CLI
    """
    application = 1
    volume = 2
    network = 3
    services = 4

def get_yaml_content(file_path):
    """ Loads the yaml content for the given file path
    :param file_path: The path of the file where yaml is located
    """
    from ruamel.yaml import YAML
    try:
        file_content = open(file_path, "r")
    except IOError:
        raise CLIError("Invalid file path %s" % file_path)
    try:
        yaml = YAML()
        content = yaml.load(file_content)
    except:
        raise CLIError("The yaml schema in the file %s is invalid" % file_path)
    file_content.close()
    return content

def get_valid_resource_type(resource):
    """ Get the valid resource type from the resource content
    :param resource: The yaml content of resource
    """
    if not len(resource.items()) == 1:
        raise CLIError("Parsing error while getting valid resource type")
    for key, value in resource.items():
        if key == "application":
            if "services" in value:
                return ResourceType.services
            return ResourceType.application
        elif key == "volume":
            return ResourceType.volume
        elif key == "network":
            return ResourceType.network
        else:
            raise CLIError('Invalid resource type found')

def construct_json_from_yaml(content):
    """ Converts the yaml content to json object
    :param content: Content to be converted to object
    """
    json_obj = json.loads(json.dumps(content))
    return json_obj

def parse_network_resource_description(content): #pylint: disable=invalid-name
    """ Gets the network resource description
    :param content: The yaml content of network resource.
    """
    None

def parse_application_resource_description(content): #pylint: disable=invalid-name
    """ Gets the application resource description
    :param content: The yaml content of application resource description.
    """
    # TO-DO Parameter Parsing
    application_name = content.get('name', None)
    if application_name is None:
        raise CLIError('Could not find application name in application description')
    return application_name


def parse_volume_provider_parameters_azure_file(volume_description_content): #pylint: disable=invalid-name
    """ Parses VolumeProviderParametersAzureFile from volume description
    :param volume_description_content: The volume description content
    """
    from azure.servicefabric.models.volume_provider_parameters_azure_file import VolumeProviderParametersAzureFile #pylint: disable=line-too-long
    account_name = volume_description_content.get('accountName', None)
    share_name = volume_description_content.get('shareName', None)
    account_key = volume_description_content.get('accountKey', None)
    if account_name is None:
        raise CLIError('Could not find account name in '
                       'Azure file share paramaters')
    if share_name is None:
        raise CLIError('Could not find share name in '
                       'Azure file share paramaters')
    return VolumeProviderParametersAzureFile(account_name=account_name,
                                             share_name=share_name,
                                             account_key=account_key)

def parse_volume_resource_description(content): #pylint: disable=invalid-name
    """ Parses volume resource description from volume content
    :param content: volume content
    """
    from azure.servicefabric.models.volume_resource_description import VolumeResourceDescription
    volume_params = content.get('params', None)
    if not volume_params is None:
        volume_provider = parse_volume_provider_parameters_azure_file(volume_params)
    volume_name = content.get('name', None)
    if volume_name is None:
        raise CLIError('Could not find volume name')
    volume_description = content.get('description', None)
    return VolumeResourceDescription(name=volume_name,
                                     description=volume_description,
                                     azure_file_parameters=volume_provider)

def parse_container_code_package_properties(code_package_content_list): #pylint: disable=invalid-name
    """ Parses service resource description from code package content
        Note: Only high level parsing is implemented here
    :param content: code package content
    """
    from azure.servicefabric.models.container_code_package_properties import ContainerCodePackageProperties  #pylint: disable=line-too-long
    from azure.servicefabric.models.resource_requirements import ResourceRequirements
    from azure.servicefabric.models.resource_requests import ResourceRequests
    from azure.servicefabric.models.resource_limits import ResourceLimits
    if  code_package_content_list is None:
        raise CLIError('Code package description is not found in service description')
    content_object_list = []
    for code_package_content in code_package_content_list:
        name = code_package_content.get('name', None)
        image = code_package_content.get('image', None)
        resources_content = code_package_content.get('resources', None)
        if name is None:
            raise CLIError('Name of the code package is not defined')
        if image is None:
            raise CLIError('Image name of the code package is not defined')
        if resources_content is None:
            raise CLIError('Resources of the code package is not defined')
        resource_requests = None
        resource_limits = None
        if not 'requests' in code_package_content:
            raise CLIError('Resource requests is not defined')
        else:
            resource_requests_content = code_package_content.get('requests')
            if not 'memory_in_gb' in resource_requests_content:
                raise CLIError('memory is not defined in resource request section')
            if not 'cpu' in resource_requests_content:
                raise CLIError('cpu not defined in resource request section')
            resource_requests = ResourceRequests(resource_requests_content.get('memory_in_gb'),
                                                 resource_requests_content.get('cpu'))
        if 'limits' in code_package_content:
            resource_limits_content = code_package_content.get('limits')
            resource_limits = ResourceLimits(resource_limits_content.get('memory_in_gb', None),
                                             resource_limits_content.get('cpu', None))
        resources = ResourceRequirements(resource_requests, resource_limits)
        code_package_object = ContainerCodePackageProperties(name=name,
                                                             image=image,
                                                             resources=resources)
        content_object_list.append(code_package_object)
    return content_object_list

def parse_network_refs(content):
    """ Parses network refs from network refs content
    :param content: network ref content
    """
    from azure.servicefabric.models.network_ref import NetworkRef
    return NetworkRef(content.get('name'))

def parse_diagnostic_ref(content):
    """ Parses diagnostic ref from diagnostic ref content
    :param content: diagnostic ref content
    """
    from azure.servicefabric.models.diagnostics_ref import DiagnosticsRef
    return DiagnosticsRef(content.get('enabled', None), content.get('sink_refs', None))

def parse_service_resource_description(content): #pylint: disable=invalid-name
    """ Parses service resource description from service content
    :param content: service content
    """
    from azure.servicefabric.models.service_resource_description import ServiceResourceDescription
    if len(content) != 1:
        raise CLIError('More that one or no service description found')
    service_content = content[0]
    diagnostics = None
    network_ref_list = None
    os_type = service_content.get('os_type', None)
    code_package_list = parse_container_code_package_properties(content.get('codePackages', None))
    if 'networkRefs' in content:
        network_ref_list = parse_network_refs(content.get('networkRefs', None))
    if 'diagnostics' in content:
        diagnostics = parse_diagnostic_ref(content.get('diagnostics', None))
    description = content.get('description', None)
    replica_count = content.get('replica_count', 0)
    health_state = content.get('health_state', None)
    name = content.get('name', None)
    if health_state not in ['Invalid', 'Ok', 'Warning', 'Unknown', 'None']:
        raise CLIError('Invalid Health state specified in service description')
    if name is None:
        raise CLIError('Name of the service is missing in service description')
    if os_type not in ['Linux', 'Windows']:
        raise CLIError('Invalid OS type in service description')
    return ServiceResourceDescription(os_type=os_type,
                                      code_packages=code_package_list,
                                      network_refs=network_ref_list,
                                      diagnostics=diagnostics,
                                      description=description,
                                      replica_count=replica_count,
                                      health_state=health_state,
                                      name=name)

def get_default_value(parameter_value):
    """ Get the default value if present on None otherwise
    : parameter_value: The parameter_value ordered dict
    """
    if "defaultValue" in parameter_value:
        return parameter_value["defaultValue"]
    return None

def parse_parameters_section(content):
    """ Parse the parameters section and return a dictionary of parameter name and value pairs
    :param content: The yaml content in ordered dict format
    """
    parameters = {}
    if "parameters" in content:
        parameters_section_content = content["parameters"]
        for parameter_key, parameter_value_dict in parameters_section_content.items():
            parameter_value = get_default_value(parameter_value_dict)
            if not parameter_value is None:
                parameters[parameter_key] = parameter_value
        return parameters
    return parameters

def get_parameter_value(param_value):
    """ If the value is specified directly returns it or replaces it
        value retrived from parameters section
    """
    # Still need to implement this
    return param_value

def create_deployment_resource(client, file_paths):
    """ Validates and deploys all the yaml resource files
    :param file_paths: Comma seperated file paths of all the yaml files
    """
    file_path_list = file_paths.split(',')
    volume_description_list = []
    service_description_list = []
    application_description = None
    for file_path in file_path_list:
        content = get_yaml_content(file_path)
        resource_type = get_valid_resource_type(content)
        if resource_type == ResourceType.application:
            print("Application")
            print(content)
            application_description = content
        elif resource_type == ResourceType.services:
            print("Services")
            print(content)
            service_description_list.append(content.get('application').get('services'))
        elif resource_type == ResourceType.network:
            print("Network")
            print(content)
        elif resource_type == ResourceType.volume:
            print("Volume")
            print(content)
            volume_description_list.append(content.get('volume'))
    '''The order of rest calls made here should be as follows:
        1. Creation of secondary resources like volume, network, secrets etc..
        2. application resource creation'''
    deploy_volume_resources(client, volume_description_list)
    deploy_application_resource(client, application_description, service_description_list)

def deploy_application_resource(client, application_description, service_description_list):
    ''' Combines the service description into application description and triggers deployment
    :param: client: REST client
    :param: application_description: application description
    :param: service_description_list: list of service descriptions
    '''
    if application_description is None:
        raise CLIError("Application description is not provided")
    if service_description_list is []:
        raise CLIError("Service Description is not provided")
    for service_description in service_description_list:
        if 'services' in service_description:
            application_description['services'].append = service_description
        else:
            application_description['services'] = service_description
    application_description_object = construct_json_from_yaml(application_description.get('application'))
    # client.create_application_resource(application_description.get('application').get('name'), application_description_object)

def deploy_volume_resources(client, volume_description_list):
    ''' Deploys the volume descriptions one by one
    :param: client: REST client
    :param: volume_description_list: list of volume descriptions
    '''
    for volume_description in volume_description_list:
        if volume_description is None:
            raise CLIError('Volume description is not provided')
        volume_description_object = construct_json_from_yaml(volume_description.get('volume'))
        # client.create_volume_resource(volume_description.get('volume').get('name'), volume_description_object)


def init_application_resource(client, application_resource_name, file_path, timeout=60): 
    content = get_yaml_content(file_path)
    print("Content:\n")
    print(content)

def init_network_resource(client, application_resource_name, file_path, timeout=60): 
    content = get_yaml_content(file_path)
    print("Content:\n")
    print(content)

def init_volume_resource(client, application_resource_name, file_path, timeout=60): 
    content = get_yaml_content(file_path)
    print("Content:\n")
    print(content)
