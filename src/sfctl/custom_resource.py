# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Commands related to managing Service Fabric Mesh resources"""

from __future__ import print_function
from collections import OrderedDict
import enum
from inspect import currentframe, getframeinfo
import json
import os
from pathlib import Path
import shutil
import sys
from knack.util import CLIError
import yaml
import random

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

def init_volume_resource(client, volume_resource_name, volume_resource_provider='sfAzureFile'): #pylint: disable=unused-argument
    """ Initialize the volume context
    :param volume_resource_name: Volume resource name
    :param volume_resource_provider: Provider of the volume resource
    """
    fabric_root = os.path.join(os.getcwd(), "ServiceFabric")
    dir1 = os.path.join(fabric_root)
    if not os.path.exists(dir1):
        os.makedirs(dir1)

    file_path = os.path.join(fabric_root, "Resources",
                             volume_resource_name + ".yaml")

    dir2 = os.path.join(dir1, "Resources")
    if not os.path.exists(dir2):
        os.makedirs(dir2)

    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_data = OrderedDict([
        ('volume', OrderedDict([
            ('schemaVersion', '1.0.0'),
            ('name', volume_resource_name),
            ('properties', OrderedDict([
                ('description', volume_resource_name + ' description.'),
                ('provider', volume_resource_provider),
                ('azureFileParameters', OrderedDict([
                    ('shareName', 'helloWorldShare'),
                    ('accountName', 'testAccount'),
                    ('accountKey', 'xyz')
                ]))
            ]))
        ]))
    ])
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file_path:
            yaml.dump(file_data, file_path, default_flow_style=False)
            print('Volume Yaml generated is: {}'.format(file_path.name), file=sys.stderr)

def init_application_resource(client, application_resource_name, #pylint: disable=unused-argument,too-many-branches
                              add_service_name=None, delete_service_name=None,
                              containerostype='Windows'):
    """ Initialize the application context
    :param application_resource_name: Application resource name.
    :param add_service_name: Add a new service to the context with the given name.
    :param delete_service_name: Delete the service from the context with the given name.
    :param containerostype: Container OS type to be used for deployment
    """
    fabric_root = os.path.join(os.getcwd(), "ServiceFabric")
    dir1 = os.path.join(fabric_root)
    if not os.path.exists(dir1):
        os.makedirs(dir1)

    file_path = os.path.join(fabric_root, "Resources", application_resource_name + ".yaml")

    dir2 = os.path.join(dir1, "Resources")
    if not os.path.exists(dir2):
        os.makedirs(dir2)

    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_data = OrderedDict([
        ('application', OrderedDict([
            ('schemaVersion', '1.0.0'),
            ('name', application_resource_name),
            ('properties', OrderedDict([
                ('description', application_resource_name + ' description.')
            ]))
        ]))
    ])

    if not os.path.exists(file_path):
        with open(file_path, 'w') as file_path:
            yaml.dump(file_data, file_path, default_flow_style=False)
            print('Application Yaml generated is: {}'.format(file_path.name), file=sys.stderr)

    # check if any service can be added or deleted
    if add_service_name != None:
        add_service_file = os.path.join(fabric_root, "Services",
                                        application_resource_name, add_service_name,
                                        "Service.yaml")
        if os.path.exists(add_service_file):
            CLIError(add_service_name + " service yaml already present.")

        dir1 = os.path.join(os.getcwd(), "ServiceFabric", "Services")
        if not os.path.exists(dir1):
            os.makedirs(dir1)
        dir2 = os.path.join(dir1, application_resource_name)
        if not os.path.exists(dir2):
            os.makedirs(dir2)

        directory = os.path.dirname(add_service_file)
        if os.path.exists(directory):
            CLIError(directory + " directory already present.")
        os.makedirs(directory)

        # create service manifest
        filename = getframeinfo(currentframe()).filename
        dir_path = Path(filename).resolve().parent
        template_service_path = os.path.join(str(dir_path), "templates", "service.yaml")

        with open(template_service_path, "rt") as in_file:
            with open(add_service_file, 'wt') as out_file:
                for line in in_file:
                    if "ApplicationName" in line:
                        out_file.write(line.replace('ApplicationName', application_resource_name))
                    elif 'FabricServiceName' in line:
                        out_file.write(line.replace('FabricServiceName', add_service_name))
                    elif 'FabricServiceImage' in line:
                        out_file.write(line.replace('FabricServiceImage', add_service_name+'Image:Tag'))
                    elif 'OsTypeValue' in line:
                        out_file.write(line.replace('OsTypeValue', containerostype))
                    elif 'FabricServiceListener' in line:
                        out_file.write(line.replace('FabricServiceListener',
                                                    add_service_name+'Listener'))
                    elif 'FabricServiceNetworkName' in line:
                        out_file.write(line.replace('FabricServiceNetworkName',
                                                    add_service_name+'NetworkName'))
                    elif 'FabricServicePort' in line:
                        out_file.write(line.replace('FabricServicePort', str(random.randint(21001,30000))))
                    else:
                        out_file.write(line)

        print('Service Yaml generated is: {}'.format(add_service_file), file=sys.stderr)

    # check if any service can be deleted
    if delete_service_name != None:
        directory = os.path.join(fabric_root, "Services", application_resource_name, delete_service_name)
        if not os.path.exists(directory):
            CLIError(directory + " directory is not present.")
        #delete service dir
        shutil.rmtree(directory)
        #print('directory deleted is: ' + directory)

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
