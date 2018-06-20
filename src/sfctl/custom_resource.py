# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Commands related to managing Service Fabric Mesh resources"""

from collections import OrderedDict
import enum
import json
import os
from pathlib import Path
import shutil
from knack.util import CLIError
import yaml
from inspect import currentframe, getframeinfo

class ResourceType(enum.Enum):
    """ Defines the valid yaml resource types
        which are parseable by CLI
    """
    application = 1
    volume = 2
    network = 3
    services = 4

def ordered_dict_representer(self, value):

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
            if "services" in value:
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
        raise CLIError('Could not find application name in application description of %s' % file_path)
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
    volume_params = content.get('params')
    if not volume_params is None:
        parse_volume_provider_parameters_azure_file(file_path, volume_params)
    volume_name = content.get('name')
    if volume_name is None:
        raise CLIError('Could not find volume name in %s' % file_path)

def parse_resource_properties(file_path, resource_content):
    ''' Parses resource properties form resources section
    :param file_path: 
    :param: resource_content: resource content 
    '''
    if not 'memoryInGB' in resource_content:
        raise CLIError('memory is not defined in resource request section in %s' % file_path) #pylint: disable=line-too-long
    if not 'cpu' in resource_content:
        raise CLIError('cpu not defined in resource request section %s' % file_path)

def parse_container_code_package_properties(file_path, code_package_content_list): #pylint: disable=invalid-name
    """ Parses service resource description from code package content
        Note: Only high level parsing is implemented here
    :param content: code package content
    :param file_path: The path of the file currently being parsed
    """
    if  code_package_content_list is None:
        raise CLIError('Code package description is not found in service description of %s' % file_path) #pylint: disable=line-too-long
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


def parse_network_refs(file_path, content):
    """ Parses network refs from network refs content
    :param content: network ref content
    :param file_path: The path of the file currently being parsed
    """
    name = content.get('name')
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
            raise CLIError("Invalid enabled parameter defined diagnostic section in %s " % file_path)  #pylint: disable=line-too-long

def parse_service_resource_description(file_path, content): #pylint: disable=invalid-name
    """ Parses service resource description from service content
    :param content: service content
    :param file_path: The path of the file currently being parsed
    """
    if len(content) != 1:
        raise CLIError('More that one or no service description found in %s' % file_path)
    service_content = content[0]
    os_type = service_content.get('osType')
    parse_container_code_package_properties(file_path, service_content.get('codePackages'))  #pylint: disable=line-too-long
    if 'networkRefs' in content:
        parse_network_refs(file_path, service_content.get('networkRefs'))
    if 'diagnostics' in content:
        parse_diagnostic_ref(file_path, service_content.get('diagnostics'))
    if 'replicaCount' in content:
        try:
            int(content.get('replicaCount'))
        except:
            raise CLIError('Invalid replica count in service description %s' % file_path)
    health_state = service_content.get('healthState')
    name = service_content.get('name')
    if not health_state  in ['Invalid', 'Ok', 'Warning', 'Unknown', None]:
        raise CLIError('Invalid Health state specified in service description in %s' % file_path)
    if name is None:
        raise CLIError('Name of the service is missing in service description in %s' % file_path)
    if os_type not in ['Linux', 'Windows']:
        raise CLIError('Invalid OS type in service description in %s' % file_path)

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

def create_deployment_resource(client, file_paths, no_wait=False):
    """ Validates and deploys all the yaml resource files
    :param: client: REST client
    :param file_paths: Comma seperated file paths of all the yaml files
    :param no_wait: Do not wait for the long-running operation to finish.
    """
    file_path_list = file_paths.split(',')
    volume_description_list = []
    service_description_list = []
    application_description = None
    for file_path in file_path_list:
        content = get_yaml_content(file_path)
        resource_type = get_valid_resource_type(file_path, content)
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
            volume_description_list.append(content)
    '''The order of rest calls made here should be as follows:
        1. Creation of secondary resources like volume, network, secrets etc..
        2. Application resource creation'''
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
            application_description['application']['services'].append(service_description[0])
        else:
            application_description['application']['services'] = service_description
    #application_description_object = construct_json_from_yaml(OrderedDict(application_description.get('application')))
    application_description_object = construct_json_from_yaml(application_description.get('application'))
    client.create_application_resource(application_description.get('application').get('name'), application_description_object)

def deploy_volume_resources(client, volume_description_list):
    ''' Deploys the volume descriptions one by one
    :param: client: REST client
    :param: volume_description_list: list of volume descriptions
    '''
    for volume_description in volume_description_list:
        if volume_description is None:
            raise CLIError('Volume description is not provided')
        volume_description_object = construct_json_from_yaml(volume_description.get('volume'))
        client.create_volume_resource(volume_description.get('volume').get('name'), volume_description_object)

def init_volume_resource(client, volume_resource_name, volume_resource_provider='sfAzureFile', timeout=60): 
    """ Initialize the volume context
    :param volume_name: Volume resource name
    :param volume_provider: Provider of the volume resource
    """
    file_path = os.path.join(os.getcwd(), "servicefabric", "App Resources", volume_resource_name+".yaml")

    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_data = OrderedDict([
        ('volume', OrderedDict([
            ('schemaVersion', '0.0.1'),
            ('name', volume_resource_name),
            ('description', volume_resource_name + ' description.'),
            ('provider', volume_resource_provider),
            ('azureFileParameters', OrderedDict([
                ('shareName', 'helloWorldShare'),
                ('accountName', 'testAccount'),
                ('accountKey', 'xyz')
            ]))
        ]))
        ])
    with open(file_path, 'w') as file_path:
        yaml.dump(file_data, file_path, default_flow_style=False)
        #print('volume yaml created is: ' + file_path)

def init_application_resource(client, application_resource_name, add_service_name=None, delete_service_name=None, containerostype='Windows', networkreference='network', timeout=60): 
    """ Initialize the application context
    :param: client: REST client
    :param application_resource_name: Application resource name.
    :param add_service_name: Add a new service to the context with the given name.
    :param delete_service_name: Delete the service from the context with the given name.
    """
    file_path = os.path.join(os.getcwd(), "servicefabric", "App Resources", "application.yaml")

    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_data = OrderedDict([
        ('application', OrderedDict([
            ('schemaVersion', '0.0.1'),
            ('name', application_resource_name),
            ('description', application_resource_name + ' description.')]))
        ])
    with open(file_path, 'w') as file_path:
        yaml.dump(file_data, file_path, default_flow_style=False)
        #print('application yaml created is: ' + file_path)

    # check if any service can be added or deleted
    if add_service_name != None:
        add_service_file = os.path.join(os.getcwd(), add_service_name, "Service Resources", "service.yaml") #pylint: disable=line-too-long
        if os.path.exists(add_service_file):
            CLIError(add_service_name + " service yaml already present.")
        directory = os.path.dirname(add_service_file)
        if os.path.exists(directory):
            CLIError(directory + " directory already present.")
        os.makedirs(directory)

        # create service manifest
        filename = getframeinfo(currentframe()).filename
        dirPath = Path(filename).resolve().parent
        templateServicePath = os.path.join(dirPath, "templates", "service.yaml")

        with open(templateServicePath, "rt") as fin:
            with open(add_service_file, 'wt') as fout:
                for line in fin:
                    if "ApplicationName" in line:
                        fout.write(line.replace('ApplicationName', application_resource_name))
                    elif 'FabricServiceName' in line:
                        fout.write(line.replace('FabricServiceName', add_service_name))
                    elif 'FabricServiceImage' in line:
                        fout.write(line.replace('FabricServiceImage', add_service_name+'Image'))
                    elif 'OsTypeValue' in line:
                        fout.write(line.replace('OsTypeValue', containerostype))
                    elif 'FabricServiceListener' in line:
                        fout.write(line.replace('FabricServiceListener', add_service_name+'Listener'))
                    elif 'FabricServiceNetworkName' in line:
                        fout.write(line.replace('FabricServiceNetworkName', add_service_name+'NetworkName'))
                    else:
                        fout.write(line)

    # check if any service can be deleted
    if delete_service_name != None:
        directory = os.path.join(os.getcwd(), delete_service_name)
        if not os.path.exists(directory):
            CLIError(directory + " directory is not present.")
        #delete service dir
        shutil.rmtree(directory)
        #print('directory deleted is: ' + directory)

def get_application_resource(client, application_resource_name, timeout=60):
    """
    :param application_resource_name: Application resource name.
    """
    response = client.get_application_resource(application_resource_name)
    print(response)
    
def get_volume_resource(client, volume_resource_name, timeout=60):
    """
    :param volume_resource_name: Application resource name.
    """
    response = client.get_volume_resource(volume_resource_name)
    print(response)

def delete_application_resource(client, application_resource_name, timeout=60):
    """
    :param application_resource_name: Application resource name.
    """
    response = client.delete_application_resource(application_resource_name)
    print(response)

def delete_volume_resource(client, volume_resource_name, timeout=60):
    """
    :param volume_resource_name: Application resource name.
    """
    response = client.delete_volume_resource(volume_resource_name)
    print(response) 

def validate_resources(client, file_paths):
    """ Performs a high level validation of the provided yaml files
    :param file_paths: Comma seperated file paths which need to validated
    """
    file_path_list = file_paths.split(',')
    for file_path in file_path_list:
        content = get_yaml_content(file_path)
        resource_type = get_valid_resource_type(file_path, content)
        if resource_type == ResourceType.application:
            print("Application")
            print(content)
            parse_application_resource_description(file_path, content.get('application'))
            print("%s application file is valid" % file_path)
        elif resource_type == ResourceType.services:
            print("Services")
            print(content)
            parse_service_resource_description(file_path, content.get('application').get('services'))
        elif resource_type == ResourceType.network:
            print("Network")
            print(content)
        elif resource_type == ResourceType.volume:
            print("Volume")
            parse_volume_resource_description(file_path, content.get('volume'))
            print(content)
