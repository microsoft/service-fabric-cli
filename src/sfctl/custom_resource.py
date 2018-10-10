# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Custom commands for managing Service Fabric Mesh resources"""

import enum
import json
import os
from knack.util import CLIError
from sfmergeutility.sf_merge_utility import SFMergeUtility

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
    """ Gets the resource type form the file name
    """
    file_name = file_name.split('_')
    resource_type = file_name[1]
    if resource_type == "application":
        return ResourceType.application
    elif resource_type == "volume":
        return ResourceType.volume
    elif resource_type == "network":
        return ResourceType.network
    elif resource_type == "secret":
        return ResourceType.secret
    elif resource_type == "gateway":
        return ResourceType.gateway
    return None

def get_resource_name(file_name):
    """ Gets resource name form the file name
    """
    file_name = file_name.split('_')
    file_name_with_extension = file_name[2]
    resource_name = file_name_with_extension.split('.')
    return resource_name[0]

def list_files_directory(directory, extension):
    """ List files of a directory recursively w.r.t
        the extension provided
    """
    file_path_list = []
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith(extension):
                file_path_list.append(os.path.join(root, filename))
    return file_path_list

def load_json(file_path):
    """ Converts the yaml content to json object
    :param content: Content to be converted to object
    """
    with open(file_path, 'r') as file_pointer:
        content = file_pointer.read()
        json_obj = json.loads(json.loads(json.dumps(content)))
    return json_obj

def mesh_deploy(client, yaml_files_or_directory):
    """ This function
        1.SFMergeUtility to merging, converting and
            ordering the resources.
        2. Deploys the resources in the order suggested by the utility
    """
    file_path_list = []
    output_dir = os.path.join(os.getcwd(), "meshDeploy")
    if os.path.isdir(yaml_files_or_directory):
        file_path_list = list_files_directory(yaml_files_or_directory, ".yaml")
    else:
        file_path_list = yaml_files_or_directory.split(',')
    SFMergeUtility.SFMergeUtility(file_path_list, "SF_SBZ_JSON", parameterFile=None, outputDir=output_dir, prefix="", region="westus") # pylint: disable=line-too-long
    resources = list_files_directory(output_dir, ".json")
    resources.sort()
    print resources
    for resource in resources:
        resource_type = get_resource_type(os.path.basename(resource))
        resource_name = get_resource_name(os.path.basename(resource))
        if resource_type == ResourceType.application:
            application_description = load_json(resource)
            client.mesh_application.create_or_update(resource_name, application_description.get('description')) # pylint: disable=line-too-long
        elif resource_type == ResourceType.volume:
            volume_description = load_json(resource)
            client.mesh_application.create_or_update(resource_name, volume_description.get('description')) # pylint: disable=line-too-long
        elif resource_type == ResourceType.network:
            network_description = load_json(resource)
            client.mesh_network.create_or_update(resource_name, network_description.get('description')) # pylint: disable=line-too-long
        elif resource_type == ResourceType.secret:
            secret_description = load_json(resource)
            client.mesh_application.create_or_update(resource_name, secret_description.get('description')) # pylint: disable=line-too-long
        elif resource_type == ResourceType.secretValue:
            secret_value_description = load_json(resource)
            client.mesh_application.create_or_update(resource_name, secret_value_description.get('description')) # pylint: disable=line-too-long
        elif resource_type == ResourceType.gateway:
            gateway_description = load_json(resource)
            client.mesh_application.create_or_update(resource_name, gateway_description.get('description')) # pylint: disable=line-too-long
        else:
            raise CLIError('Invalid resource type found %s' %(resource))
