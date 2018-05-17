# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Custom commands for the Service Fabric naming support"""

def naming_property_put(client, name_id, property_name, # pylint: disable=too-many-arguments
                        value, custom_id_type=None, timeout=60):
    """Custom commands for creating or updating a Service Fabric property"""
    from azure.servicefabric.models.property_description import PropertyDescription

    desc = PropertyDescription(property_name=property_name,
                               value=value,
                               custom_type_id=custom_id_type)
    client.put_property(name_id, desc, timeout=timeout)
