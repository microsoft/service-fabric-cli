# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Custom commands for managing Service Fabric Mesh resources"""

from __future__ import print_function

import os
import shutil
from knack.util import CLIError
from sfmergeutility import SFMergeUtility
from sfmergeutility.utility import ResourceType, get_resource_name, get_resource_type, list_files_in_directory, load_json # pylint: disable=line-too-long

def deploy_resource(client, resource):
    """ Deploys the specified resource to the connected cluster
    :param client: (class) Auto generated client from swagger specification
    :param resource: (str) Relative/absolute path of the resource file
    """
    resource_type = get_resource_type(resource)
    resource_name = get_resource_name(resource)

    print('Creating resource: ', resource_name, 'of type: ', resource_type.name)

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

def mesh_deploy(client, input_yaml_files, parameters=None):
    """ This function
        1. Uses sfmergeutility to merge, convert, and
        order the resources
        2. Deploys the resources in the order suggested by the utility
    :param client: (class) Auto generated client from swagger specification
    :param input_yaml_files: (str) Relative/absolute directory path or comma seperated relative/absolute file paths of the yaml resource files  # pylint: disable=line-too-long
    """
    file_path_list = []

    if os.path.isdir(input_yaml_files):
        if not os.path.exists(input_yaml_files):
            raise CLIError('The specified directory "%s" does not exist or you do not have access to it' %(input_yaml_files)) # pylint: disable=line-too-long
        file_path_list = list_files_in_directory(input_yaml_files, ".yaml")

    else:
        file_path_list = input_yaml_files.split(',')
        for file_path in file_path_list:
            if not os.path.exists(file_path):
                raise CLIError('The specified file "%s" does not exist or you do not have access to it' %(file_path)) # pylint: disable=line-too-long

    output_dir = os.path.join(os.getcwd(), "meshDeploy")
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir, ignore_errors=True)

    SFMergeUtility.sf_merge_utility(file_path_list, "SF_SBZ_JSON", parameters=parameters, output_dir=output_dir, prefix="") # pylint: disable=line-too-long
    resources = list_files_in_directory(output_dir, ".json")
    resources.sort()
    for resource in resources:
        deploy_resource(client, resource)
