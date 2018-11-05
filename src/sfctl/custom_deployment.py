# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Custom commands for managing Service Fabric Mesh resources"""

from __future__ import print_function

import enum
import json
import os
import shutil
from knack.util import CLIError
from sfmergeutility import SFMergeUtility

class ResourceType(enum.Enum):
    """ Defines the valid yaml resource types
        which are parseable by CLI
    """
    application = 1
    volume = 2
    network = 3
    secret = 4
    secretValue = 5
    gateway = 6

def get_resource_type(file_name):
    """ Gets the resource type from the file name
    :param str file_name: Path of the file
    """
    file_name = os.path.basename(file_name)
    file_name_splitted = file_name.split('_')
    if len(file_name_splitted) < 3:
        raise CLIError('Invalid resource file name %s. The file name should be of format id_resourcetype_resourcename.json' %(file_name)) # pylint: disable=line-too-long
    resource_type = file_name_splitted[1]
    try:
        return ResourceType[resource_type]
    except:
        raise CLIError('The resource type %s is unknown' %(resource_type))

def get_resource_name(file_name):
    """ Gets resource name from the file name
    :param str file_name: Path of the file
    """
    file_name = os.path.basename(file_name)
    file_name_splitted = file_name.split('_')
    if len(file_name_splitted) < 3:
        raise CLIError('Invalid resource file name %s. The file name should be of format id_resourcetype_resourcename.json' %(file_name)) # pylint: disable=line-too-long
    file_name_with_extension = file_name_splitted[2]
    resource_name = file_name_with_extension.split('.')
    return resource_name[0]

def list_files_in_directory(directory, extension):
    """ List files of a directory recursively w.r.t
        the extension provided
    :param str directory: The directory path for which you want to list files
    :param str extension: The file extension of the files you want to return
    """
    file_path_list = []
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith(extension):
                file_path_list.append(os.path.join(root, filename))
    return file_path_list

def load_json(file_path):
    """ Converts the yaml content to json object
    :param content: Content to be converted to json object
    """
    with open(file_path, 'r') as file_pointer:
        content = file_pointer.read()
        json_obj = json.loads(json.loads(json.dumps(content)))
    return json_obj

def deploy_resource(client, resource):
    """ Deploys the specified resource to cluster
    :param obj client: Auto generated client
    :param str resource: Path of the resource file
    """
    resource_type = get_resource_type(resource)
    resource_name = get_resource_name(resource)
    print("Creating resource: ", resource_name, "of type: ", resource_type.name)
    if resource_type == ResourceType.application:
        application_description = load_json(resource)
        client.mesh_application.create_or_update(resource_name, application_description.get('description')) # pylint: disable=line-too-long
    elif resource_type == ResourceType.volume:
        volume_description = load_json(resource)
        client.mesh_volume.create_or_update(resource_name, volume_description.get('description')) # pylint: disable=line-too-long
    elif resource_type == ResourceType.network:
        network_description = load_json(resource)
        client.mesh_network.create_or_update(resource_name, network_description.get('description').get('name'), network_description.get('description').get('properties')) # pylint: disable=line-too-long
    elif resource_type == ResourceType.secret:
        secret_description = load_json(resource)
        client.mesh_secret.create_or_update(resource_name, secret_description.get('description').get('properties'), secret_description.get('description').get('name')) # pylint: disable=line-too-long
    elif resource_type == ResourceType.secretValue:
        secret_value_description = load_json(resource)
        fully_qualified_resource_name = secret_value_description.get('fullyQualifiedResourceName').split('/') # pylint: disable=line-too-long
        secret_value_resource_name = fully_qualified_resource_name[1]
        client.mesh_secret_value.add_value(resource_name, secret_value_resource_name, secret_value_description.get('description').get('name'), secret_value_description.get('description').get('properties').get('value')) # pylint: disable=line-too-long
    elif resource_type == ResourceType.gateway:
        gateway_description = load_json(resource)
        client.mesh_gateway.create_or_update(resource_name, gateway_description.get('description')) # pylint: disable=line-too-long
    else:
        raise CLIError('Invalid resource type found %s' %(resource))

def mesh_deploy(client, input_yaml_file_paths, parameters=None):
    """ This function
        1.Uses sfmergeutility to merge, convert and
            order the resources.
        2. Deploys the resources in the order suggested by the utility
    """
    file_path_list = []
    if os.path.isdir(input_yaml_file_paths):
        if not os.path.exists(input_yaml_file_paths):
            raise CLIError("The specified directory %s does not exist or you do not have access to it" %(input_yaml_file_paths)) # pylint: disable=line-too-long
        file_path_list = list_files_in_directory(input_yaml_file_paths, ".yaml")
    else:
        file_path_list = input_yaml_file_paths.split(',')
        for file_path in file_path_list:
            if not os.path.exists(file_path):
                raise CLIError("The specified file %s does not exist or you do not have access to it" %(file_path)) # pylint: disable=line-too-long
    output_dir = os.path.join(os.getcwd(), "meshDeploy")
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir, ignore_errors=True)
    SFMergeUtility.sf_merge_utility(file_path_list, "SF_SBZ_JSON", parameter_file=parameters, output_dir=output_dir, prefix="") # pylint: disable=line-too-long
    resources = list_files_in_directory(output_dir, ".json")
    resources.sort()
    for resource in resources:
        deploy_resource(client, resource)
