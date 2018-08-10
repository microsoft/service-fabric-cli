# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Commands related to managing Service Fabric Mesh resources"""

from __future__ import print_function
import enum
import json
import os
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

def create_deployment_resource(client, file_paths_or_directory):
    """ Validates and deploys all the yaml resource files
    :param client: REST client
    :param file_paths_or_directory: Comma seperated file paths of all the yaml files
    """
    file_path_list = []
    if os.path.isdir(file_paths_or_directory):
        for root, _, files in os.walk(file_paths_or_directory):
            for filename in files:
                if filename.endswith(".yaml"):
                    file_path_list.append(os.path.join(root, filename))
    else:
        file_path_list = file_paths_or_directory.split(',')
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
