# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Commands related to managing Service Fabric Mesh resources"""

from __future__ import print_function
from collections import OrderedDict
import enum
import json
import sys
from knack.util import CLIError
import yaml

class ResourceType(enum.Enum):
    """ Defines the valid yaml resource types
        which are parseable by CLI
    """
    application = 1
    volume = 2
    network = 3
    services = 4

def ordered_dict_representer(self, value): #pylint: disable=missing-docstring

    return self.represent_mapping('tag:yaml.org,2002:map', value.items())

yaml.add_representer(OrderedDict, ordered_dict_representer)

def get_yaml_content(file_path):
    """ Loads the yaml content for the given file path
    :param file_path: The path of the file where yaml is located
    """
    try:
        file_content = open(file_path, "r")
    except IOError:
        raise CLIError("Invalid file path %s" % file_path)
    try:
        content = yaml.safe_load(file_content)
    except:
        raise CLIError("The yaml schema in the file %s is invalid" % file_path)
    file_content.close()
    return content

def get_valid_resource_type(file_path, resource):
    """ Get the valid resource type from the resource content
    :param resource: The yaml content of resource
    """
    if not len(resource.items()) == 1:
        raise CLIError("Parsing error while getting valid resource type in %s" % file_path)
    for key, value in resource.items():
        if key == "application":
            if "services" in value.get('properties'):
                return ResourceType.services
            return ResourceType.application
        elif key == "volume":
            return ResourceType.volume
        elif key == "network":
            return ResourceType.network
        else:
            raise CLIError("Invalid resource type found in %s" % file_path)

def construct_json_from_yaml(content):
    """ Converts the yaml content to json object
    :param content: Content to be converted to object
    """
    json_obj = json.loads(json.dumps(content))
    return json_obj

def parse_application_resource_description(file_path, content): #pylint: disable=invalid-name
    """ Gets the application resource description
    :param content: The yaml content of application resource description.
    """
    # TO-DO Parameter Parsing
    application_name = content.get('name')
    if application_name is None:
        raise CLIError('Could not find application name '
                       'in application description of %s' % file_path)
    return application_name

def parse_volume_provider_parameters_azure_file(file_path, volume_description_content): #pylint: disable=invalid-name
    """ Parses VolumeProviderParametersAzureFile from volume description
    :param volume_description_content: The volume description content
    :param file_path: The path of the file currently being parsed
    """
    account_name = volume_description_content.get('accountName')
    share_name = volume_description_content.get('shareName')
    if account_name is None:
        raise CLIError('Could not find account name in '
                       'Azure file share paramaters of %s' % file_path)
    if share_name is None:
        raise CLIError('Could not find share name in '
                       'Azure file share paramaters of %s' % file_path)

def parse_volume_resource_description(file_path, content): #pylint: disable=invalid-name
    """ Parses volume resource description from volume content
    :param content: volume content
    :param file_path: The path of the file currently being parsed
    """
    properties = content.get('properties')
    if properties is None:
        raise CLIError('Could not find volume properties section defined in %s' % file_path)
    volume_params = content.get('properties').get('params')
    if not volume_params is None:
        parse_volume_provider_parameters_azure_file(file_path, volume_params)
    volume_name = content.get('name')
    if volume_name is None:
        raise CLIError('Could not find volume name in %s' % file_path)

def parse_resource_properties(file_path, resource_content):
    ''' Parses resource properties form resources section
    :param file_path
    :param resource_content: resource content
    '''
    if not 'memoryInGB' in resource_content:
        raise CLIError('memory is not defined in '
                       'resource request section in %s' % file_path)
    if not 'cpu' in resource_content:
        raise CLIError('cpu not defined in resource request section %s' % file_path)

def parse_container_code_package_properties(file_path, code_package_content_list): #pylint: disable=invalid-name
    """ Parses service resource description from code package content
        Note: Only high level parsing is implemented here
    :param content: code package content
    :param file_path: The path of the file currently being parsed
    """
    if  code_package_content_list is None:
        raise CLIError('Code package description is not found '
                       'in service description of %s' % file_path)
    for code_package_content in code_package_content_list:
        name = code_package_content.get('name')
        image = code_package_content.get('image')
        resources_content = code_package_content.get('resources')
        if name is None:
            raise CLIError('Name of the code package is not defined in %s' % file_path)
        if image is None:
            raise CLIError('Image name of the code package is not defined in %s' % file_path)
        if resources_content is None:
            raise CLIError('Resources of the code package is not defined in %s' % file_path)
        if not 'requests' in code_package_content.get('resources'):
            raise CLIError('Resource requests is not defined in %s' % file_path)
        else:
            resource_requests_content = code_package_content.get('resources').get('requests')
            parse_resource_properties(file_path, resource_requests_content)
        if 'limits' in code_package_content.get('resources'):
            resource_limits_content = code_package_content.get('resources').get('limits')
            parse_resource_properties(file_path, resource_limits_content)


def parse_network_refs(file_path, network_list):
    """ Parses network refs from network refs content
    :param content: network ref content
    :param file_path: The path of the file currently being parsed
    """
    for network in network_list:
        name = network.get('name')
        if name is None:
            raise CLIError("Name is not defined in network ref section in %s" % file_path)

def parse_diagnostic_ref(file_path, content):
    """ Parses diagnostic ref from diagnostic ref content
    :param content: diagnostic ref content
    :param file_path: The path of the file currently being parsed
    """
    if 'enabled' in content:
        try:
            bool(content.get('enabled'))
        except:
            raise CLIError('Invalid enabled parameter '
                           'defined diagnostic section in %s ' % file_path)

def parse_service_resource_description(file_path, content): #pylint: disable=invalid-name
    """ Parses service resource description from service content
    :param content: service content
    :param file_path: The path of the file currently being parsed
    """
    if len(content) != 1:
        raise CLIError('More that one or no service description found in %s' % file_path)
    service_content = content[0]
    service_properties = service_content.get('properties')
    if service_properties is None:
        raise CLIError('Could not find volume properties section defined in %s' % file_path)
    os_type = service_properties.get('osType')
    parse_container_code_package_properties(file_path,
                                            service_properties.get('codePackages'))
    if 'networkRefs' in service_properties:
        parse_network_refs(file_path, service_properties.get('networkRefs'))
    if 'diagnostics' in service_properties:
        parse_diagnostic_ref(file_path, service_properties.get('diagnostics'))
    if 'replicaCount' in service_properties:
        try:
            int(service_properties.get('replicaCount'))
        except:
            raise CLIError('Invalid replica count in service description %s' % file_path)
    health_state = service_properties.get('healthState')
    name = service_content.get('name')
    if not health_state  in ['Invalid', 'Ok', 'Warning', 'Unknown', None]:
        raise CLIError('Invalid Health state specified in service description in %s' % file_path)
    if name is None:
        raise CLIError('Name of the service is missing in service description in %s' % file_path)
    if os_type not in ['Linux', 'Windows']:
        raise CLIError('Invalid OS type in service description in %s' % file_path)

def create_deployment_resource(client, file_paths):
    """ Validates and deploys all the yaml resource files
    :param client: REST client
    :param file_paths: Comma seperated file paths of all the yaml files
    """
    file_path_list = file_paths.split(',')
    volume_description_list = []
    service_description_list = []
    application_description = None
    for file_path in file_path_list:
        content = get_yaml_content(file_path)
        resource_type = get_valid_resource_type(file_path, content)
        if resource_type == ResourceType.application:
            application_description = content
        elif resource_type == ResourceType.services:
            service_description_list.append(content.get('application').get('properties').get('services')) #pylint: disable=line-too-long
        elif resource_type == ResourceType.volume:
            volume_description_list.append(content)
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
    if not service_description_list:
        raise CLIError("Service Description is not provided")
    application_description.get('application').get('properties')['services'] = []
    for service_description in service_description_list:
        application_description.get('application').get('properties').get('services').append(service_description[0]) #pylint: disable=line-too-long
    application_description_object = construct_json_from_yaml(application_description.get('application')) #pylint: disable=line-too-long
    client.create_application_resource(application_description.get('application').get('name'),
                                       application_description_object)

def deploy_volume_resources(client, volume_description_list):
    ''' Deploys the volume descriptions one by one
    :param: client: REST client
    :param: volume_description_list: list of volume descriptions
    '''
    for volume_description in volume_description_list:
        if volume_description is None:
            raise CLIError('Volume description is not provided')
        volume_description_object = construct_json_from_yaml(volume_description.get('volume'))
        client.create_volume_resource(volume_description.get('volume').get('name'),
                                      volume_description_object)

def create_volume_resource(client, file_path):
    """ Create a volume resource for the provided yaml file
    :param file_path: File path of the volume resource which needs to be created
    """
    volume_description = get_yaml_content(file_path)
    resource_type = get_valid_resource_type(file_path, volume_description)

    if not resource_type == ResourceType.volume:
        raise CLIError('The file %s is not a valid volume resource file' % file_path)
    volume_description_object = construct_json_from_yaml(volume_description.get('volume'))
    client.create_volume_resource(volume_description.get('volume').get('name'),
                                  volume_description_object)

def validate_resources(client, file_paths): #pylint: disable=unused-argument
    """ Performs a high level validation of the provided yaml files
    :param file_paths: Comma seperated file paths which need to validated
    """
    file_path_list = file_paths.split(',')
    for file_path in file_path_list:
        content = get_yaml_content(file_path)
        resource_type = get_valid_resource_type(file_path, content)
        if resource_type == ResourceType.application:
            parse_application_resource_description(file_path, content.get('application'))
            print('{} application file is valid'.format(file_path), file=sys.stderr)
        elif resource_type == ResourceType.services:
            parse_service_resource_description(file_path, content.get('application').get('properties').get('services')) #pylint: disable=line-too-long
            print('{} service file is valid'.format(file_path), file=sys.stderr)
        elif resource_type == ResourceType.volume:
            parse_volume_resource_description(file_path, content.get('volume'))
            print('{} volume file is valid'.format(file_path), file=sys.stderr)
