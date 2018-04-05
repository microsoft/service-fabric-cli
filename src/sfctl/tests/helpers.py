# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Shared helpers for mocks and utils used among all tests"""

import os
import xml.etree.ElementTree as ET
from mock import MagicMock


APP_PATH = os.environ.get('SF_TEST_APP_PATH', False)
ENDPOINT = os.environ.get('SF_TEST_ENDPOINT', False)

MOCK_CONFIG = MagicMock()


def mock_config_values(section, name, fallback):
    """Validate and mock config returns"""
    if section != 'servicefabric':
        raise ValueError('Cannot retrieve non service fabric config value')
    if name == 'endpoint':
        return os.environ.get('SF_TEST_ENDPOINT', False)
    if name == 'security':
        return 'none'
    return fallback


MOCK_CONFIG.return_value.get.side_effect = mock_config_values

# XMLNS for fabric manifests
XML_NS = {'fabric': 'http://schemas.microsoft.com/2011/01/fabric'}


def parse_app_version(xml_file):
    """Parse application type version from application manifest"""
    root = ET.parse(xml_file).getroot()
    version = root.attrib.get('ApplicationTypeVersion', None)
    if not version:
        raise ValueError('Could not parse application type version')
    return version


def parse_app_type(xml_file):
    """Parse application type name from application manifest"""
    root = ET.parse(xml_file).getroot()
    app_type = root.attrib.get('ApplicationTypeName', None)
    if not app_type:
        raise ValueError('Could not parse application type name')
    return app_type


def find_service_manifest(xml_file):
    """Find the path to the first service manifest for an application"""
    root = ET.parse(xml_file).getroot()

    import_elem = root.find('fabric:ServiceManifestImport', XML_NS)
    if import_elem is None:
        raise ValueError('Could not find service manifest import section')

    ref_elem = import_elem.find('fabric:ServiceManifestRef', XML_NS)
    if ref_elem is None:
        raise ValueError('Could not find service manifest reference section')

    manifest_name = ref_elem.attrib.get('ServiceManifestName', None)
    if not manifest_name:
        raise ValueError('Could not find service manifest name')
    return os.path.join(os.path.dirname(xml_file), manifest_name,
                        'ServiceManifest.xml')


def parse_service_type(xml_file):
    """Determines the first available service type and the associated
    type name"""
    root = ET.parse(xml_file).getroot()
    service_type = root.find('fabric:ServiceTypes', XML_NS)
    if service_type is None:
        raise ValueError('Could not find service types in service manifest')
    service_type_kind = None
    if 'StatelessServiceType' in service_type[0].tag:
        service_type_kind = 'stateless'
    else:
        # For now we only support stateless services for service creation
        raise ValueError('Unsupported service type')
    service_type_name = service_type[0].attrib.get('ServiceTypeName', None)
    if not service_type_name:
        raise ValueError('Could not find service type name')

    return service_type_kind, service_type_name
