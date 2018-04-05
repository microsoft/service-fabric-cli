# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Help documentation for Service Fabric property commands."""

from knack.help_files import helps

# If the parameter name doesn't match the actual parameter name,
# no information will be provided in the help page

# To keep newlines in the help documentation, follow this format:
# long-summary: |
#    Following are the ...
#    1. text
#    2. text

helps['property put'] = """
    type: command
    short-summary: Creates or updates a Service Fabric property.
    long-summary: Creates or updates the specified Service Fabric property under a given name.
    parameters:
        - name: --name-id
          type: string
          short-summary: The Service Fabric name, without the 'fabric:' URI scheme.
        - name: --property-name
          type: string
          short-summary: The name of the Service Fabric property.
        - name: --value
          type: string
          short-summary: Describes a Service Fabric property value. This is a JSON string.
          long-summary: The json string has two fields, the 'Kind' of the data, and the 'Value'
            of the data. The 'Kind' value must be the first item to appear in the JSON string,
            and can be values 'Binary', 'Int64', 'Double', 'String', or 'Guid'. The value should
            be serialize-able to the given types. Both 'Kind' and 'Data' values should be
            provided as strings.
        - name: --custom-id-type
          type: string
          short-summary: The property's custom type id. Using this property, the user
            is able to tag the type of the value of the property.
"""