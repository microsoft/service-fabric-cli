# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Commands related to managing Service Fabric Mesh resources"""

from knack.util import CLIError
from pathlib import Path
import os
import yaml
import shutil
from collections import OrderedDict

def ordered_dict_representer(self, value):
    return self.represent_mapping('tag:yaml.org,2002:map', value.items())

yaml.add_representer(OrderedDict, ordered_dict_representer)

def get_yaml_content(file_path):
    """ Loads the yaml content for the given file path
    :param file_path: The path of the file where yaml is located
    """
    from ruamel.yaml import YAML
    file_content = open(file_path, "r")
    yaml = YAML()
    content = yaml.load(file_content)
    file_content.close()
    return content


def get_valid_resource_type(resource, valid_resource_types):
    """ Get the valid resource type from the resource content
    :param resource: The yaml content of resource in ordered dict format
    :param valid_resource_types: The list of valid resource types
    """
    if not "type" in resource:
        return None
    elif not resource["type"] in valid_resource_types:
        return None
    else:
        return resource["type"]
    raise CLIError("Code path should not have come here")

def get_resource_description_list(content, requested_resource_type):
    """ Get the appropriate resource description based on the resource type
    :param content: The yaml content in ordered dict format.
    :param resource_type: The resource type you want to get information.
    """
    valid_resource_types = [
        "Microsoft.ServiceFabric/applications",
        "Microsoft.ServiceFabric/networks",
        "Microsoft.ServiceFabric/volumes",
        "Microsoft.ServiceFabric/secrets"]
    resources_section = content["resources"]
    resource_description_list = []
    for resource in resources_section:
        current_resource_type = get_valid_resource_type(resource, valid_resource_types)
        if current_resource_type is None:
            raise CLIError("Invalid resource type found in the yaml definition")
        else:
            if requested_resource_type == current_resource_type:
                resource_description_list.append(resource)
    return resource_description_list


def parse_network_resource_description_list(content):
    """ Gets the network resource description
    :param content: The yaml content in ordered dict format.
    """
    return get_resource_description_list(content, "Microsoft.ServiceFabric/networks")

def parse_application_resource_description(content):
    """ Gets the application resource description
    :param content: The yaml content in ordered dict format.
    """
    application_resource_description_list = get_resource_description_list(
        content, "Microsoft.ServiceFabric/applications")
    if not len(application_resource_description_list) == 1:
        raise CLIError("There should be only one application resource defined")
    return application_resource_description_list[0]


def parse_volume_provider_parameters_azure_file(volume_description_content):
    """ Parses VolumeProviderParametersAzureFile from volume description in ordered dict format
    :param volume_description_content: The volume description content in ordered dict format
    """


def parse_volume_resource_description_list(content):
    """ Gets the volume resource description
    :param content: The yaml content in ordered dict format.
    """
    from azure.servicefabric.models.volume_resource_description import VolumeResourceDescription
    from azure.servicefabric.models.volume_provider_parameters_azure_file import VolumeProviderParametersAzureFile

    volume_resource_description_list_content = get_resource_description_list(content, "Microsoft.ServiceFabric/volumes")
    
    volume_resource_description_list = []
    for volume_resource_description_content in volume_resource_description_list_content:
        None
    return volume_resource_description_list

def parse_secret_resource_description_list(content):
    """ Gets the secret resource description
    :param content: The yaml content in ordered dict format.
    """
    return get_resource_description_list(content, "Microsoft.ServiceFabric/secrets")

def get_default_value(parameter_value):
    """ Get the default value if present on None otherwise
    : parameter_value: The parameter_value ordered dict
    """
    if "defaultValue" in parameter_value:
        return parameter_value["defaultValue"]
    else:
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
    else:
        return parameters

def get_parameter_value(param_value):
    """ If the value is specified directly returns it or replaces it
        value retrived from parameters section
    """
    # Still need to implement this
    return param_value

def create_deployment_resource(client, application_resource_name, file_path, timeout=60): 
    from azure.servicefabric.models.application_resource_description import ApplicationResourceDescription
    content = get_yaml_content(file_path)
    print("Content:\n")
    print(content)

def init_network_resource(client, application_resource_name, file_path, timeout=60): 
    from azure.servicefabric.models.application_resource_description import ApplicationResourceDescription
    content = get_yaml_content(file_path)
    print("Content:\n")
    print(content)

def init_volume_resource(client, volume_name, volume_provider='sfAzureFile', timeout=60): 
    """ Initialize the volume context
    :param volume_name: Volume resource name
    :param volume_provider: Provider of the volume resource
    """
    file_path = os.path.join(os.getcwd(), "servicefabric", "volume.yaml")

    #if volume yaml doesn't exists, create    
    if not Path(file_path).exists():
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        file_data = OrderedDict([
            ('volume', OrderedDict([
            ('schemaVersion','0.0.1'),
            ('name', volume_name),
            ('description' , volume_name + ' description.'),
            ('sharingType', 'shared'),
            ('provider', volume_provider),
            ('params', OrderedDict([
                ('shareName', 'helloWorldShare'),
                ('accountName', 'testAccount'),
                ('accountKey', 'xyz')
            ]))
            ]))            
            ]
        )
        with open(file_path, 'w') as file_path:
            yaml.dump(file_data, file_path, default_flow_style=False)


def init_application_resource(client, application_resource_name, add_service_name=None, delete_service_name=None, containerostype='Windows', networkreference='network', timeout=60): 
    """ Initialize the application context
    :param application_resource_name: Application resource name.
    :param add_service_name: Add a new service to the context with the given name.
    :param delete_service_name: Delete the service from the context with the given name.
    """    
    file_path = os.path.join(os.getcwd(), "servicefabric", "application.yaml")

    #if application yaml doesn't exists, create    
    if not Path(file_path).exists():
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        file_data = OrderedDict([
            ('application', OrderedDict([
            ('schemaVersion','0.0.1'),
            ('name', application_resource_name),
            ('description' , application_resource_name + ' description.')]))
            ]
        )
        with open(file_path, 'w') as file_path:
            yaml.dump(file_data, file_path, default_flow_style=False)
        
    # check if any service can be added or deleted
    if add_service_name != None:
        add_service_file = os.path.join(os.getcwd(), "serviceresource", add_service_name, "service.yaml")
        if Path(add_service_file).exists:
            CLIError(add_service_name + " service manifest already present.")
        
        directory = os.path.dirname(add_service_file)            
        if os.path.exists(directory):
            CLIError(directory + " directory already present.")
        os.makedirs(directory)            

        # create service manifest
        file_data = OrderedDict([
            ('service', OrderedDict([
                ('name', add_service_name),
                ('description', add_service_name + ' description.'),
                ('osType', containerostype),
                ('codePackages', OrderedDict([
                    ('name', add_service_name),
                    ('image', add_service_name),
                    ('endpoints', OrderedDict([
                        ('name', add_service_name + 'Listener'),
                        ('port', 20003)
                    ])),
                    ('resources', OrderedDict([
                        ('requests', OrderedDict([
                            ('cpu', '0.5'),
                            ('memoryInGB', '1')    
                        ]))                        
                    ]))                    
                ])),
                ('replicaCount', '1'),
                ('networkRefs', OrderedDict([
                    ('name', add_service_name + networkreference)
                ]))
            ])
            )
        ])
       
        with open(add_service_file, 'w') as add_service_file:
            yaml.dump(file_data, add_service_file, default_flow_style=False)        
       
            
    # check if any service can be deleted
    if delete_service_name != None:
        delete_service_file = os.path.join(os.getcwd(), "serviceresource", delete_service_name, "service.yaml")

        directory = os.path.dirname(delete_service_file)            
        if not os.path.exists(directory):
            CLIError(directory + " directory is not present.")
        # delete service manifest and dir            
        shutil.rmtree(directory)


