# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Full command and scenario tests"""

from unittest import skipUnless
from mock import patch
from knack.testsdk import (ScenarioTest, JMESPathCheck, NoneCheck)
from sfctl.entry import cli
from sfctl.tests.helpers import (ENDPOINT, MOCK_CONFIG)


class ServiceFabricScenarioTests(ScenarioTest):
    """Scenario tests for Service Fabric commands"""

    def __init__(self, method_name):
        cli_env = cli()
        super(ServiceFabricScenarioTests, self).__init__(cli_env, method_name)

    @skipUnless(ENDPOINT, 'Requires live cluster')
    @patch('sfctl.config.CLIConfig', new=MOCK_CONFIG)
    def test_cluster_select_no_security(self):
        """Select a cluster with no security"""
        self.cmd('cluster select --endpoint {0}'.format(ENDPOINT),
                 checks=[NoneCheck()])

    @skipUnless(ENDPOINT, 'Requires live cluster')
    @patch('sfctl.config.CLIConfig', new=MOCK_CONFIG)
    def test_cluster_property_list(self):
        """List System cluster properties"""
        self.cmd('property list --name-id {0}'.format("System"),
                 checks=[JMESPathCheck(
                     'properties', []
                 )])

    @skipUnless(ENDPOINT, 'Requires live cluster')
    @patch('sfctl.config.CLIConfig', new=MOCK_CONFIG)
    def test_cluster_property_list_bad_name(self):  # pylint: disable=invalid-name
        """List System cluster properties
         for non existent Service Fabric name"""
        self.cmd('property list --name-id {0}'.format("NonExistentName"),
                 expect_failure=True)

    @skipUnless(ENDPOINT, 'Requires live cluster')
    @patch('sfctl.config.CLIConfig', new=MOCK_CONFIG)
    def test_cluster_property_get_bad_property(self):  # pylint: disable=invalid-name
        """Get System cluster property
         for non existent property"""
        self.cmd('property get --name-id {0} --property-name {1}'
                 .format("System", "NonExistentPropertyName"),
                 expect_failure=True)

    @skipUnless(ENDPOINT, 'Requires live cluster')
    @patch('sfctl.config.CLIConfig', new=MOCK_CONFIG)
    def test_cluster_property_get_bad_name(self):  # pylint: disable=invalid-name
        """Get System cluster property for
         non existent Service Fabric name"""
        self.cmd('property get --name-id {0} --property-name {1}'
                 .format("NonExistentName", "Test"),
                 expect_failure=True)
