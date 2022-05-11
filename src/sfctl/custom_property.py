# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Custom commands for the Service Fabric naming support"""

def naming_property_put(client, name_id, property_name,  # pylint: disable=too-many-arguments
                        value, custom_id_type=None, timeout=60):
    """Custom commands for creating or updating a Service Fabric property"""

    desc = {"PropertyName" : property_name,
            "Value" :value,
            "CustomTypeId" : custom_id_type}
    client.put_property(name_id, desc, timeout=timeout)

def delete_property(client, name_id, property_name, timeout=60):
    """Deletes the specified Service Fabric property.
        Deletes the specified Service Fabric property under a given name. A property must be created
        before it can be deleted.

        :param name_id: The Service Fabric name, without the 'fabric:' URI scheme.
        :type name_id: str
        :param property_name: Specifies the name of the property to get.
        :paramtype property_name: str
        """
    client.delete_property(name_id, property_name=property_name, timeout=timeout)

def get_property_info(client, name_id, property_name, timeout=60):
    """Gets the specified Service Fabric property.

        Gets the specified Service Fabric property under a given name. This will always return both
        value and metadata.

        :param name_id: The Service Fabric name, without the 'fabric:' URI scheme.
        :type name_id: str
        :param property_name: Specifies the name of the property to get.
        """
    return client.get_property_info(name_id, property_name=property_name, timeout=timeout)


def get_property_info_list(client, name_id, include_values=False, continuation_token=None, timeout=60):
    """Gets information on all Service Fabric properties under a given name.
        A Service Fabric name can have one or more named properties that store custom information. This
        operation gets the information about these properties in a paged list. The information includes
        name, value, and metadata about each of the properties.

        :param name_id: The Service Fabric name, without the 'fabric:' URI scheme.
        :type name_id: str
        :param include_values: Allows specifying whether to include the values of the properties
                returned. True if values should be returned with the metadata; False to return only property
                metadata. Default value is False.
        :paramtype include_values: bool
        :param continuation_token: The continuation token parameter is used to obtain next
                set of results. A continuation token with a non-empty value is included in the response of the
                API when the results from the system do not fit in a single response. When this value is passed
                to the next API call, the API returns next set of results. If there are no further results,
                then the continuation token does not contain a value. The value of this parameter should not be
                URL encoded. Default value is None.
        :paramtype continuation_token: str
        """
    return client.get_property_info_list(name_id, include_values=include_values, timeout=timeout,
                                         continuation_token_parameter=continuation_token)
