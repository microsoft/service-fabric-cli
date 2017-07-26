# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Full command and scenario tests"""

import os
from unittest import skip
from mock import patch, MagicMock
from knack.testsdk import ScenarioTest, JMESPathCheck, NoneCheck
from sfctl.entry import cli


ENDPOINT = os.environ.get('SF_TEST_ENDPOINT', 'http://localhost:19080')

MOCK_CLASS = MagicMock()
def mock_config_values(section, name, fallback):
    """Validate and mock config returns"""
    if section != 'servicefabric':
        raise ValueError('Cannot retrieve non service fabric config value')
    if name == 'endpoint':
        return ENDPOINT
    if name == 'security':
        return 'none'
    return fallback
MOCK_CLASS.return_value.get.side_effect = mock_config_values

class ServiceFabricScenarioTests(ScenarioTest):
    """Scenario tests for Service Fabric commands"""

    def __init__(self, method_name):
        cli_env = cli()
        super(ServiceFabricScenarioTests, self).__init__(cli_env, method_name)

    @skip('Long scenario test only')
    @patch('sfctl.config.CLIConfig', new=MOCK_CLASS)
    def cluster_select_no_security_test(self):
        """Select a cluster with no security"""
        self.cmd('cluster select --endpoint {0}'.format(ENDPOINT),
                 checks=NoneCheck())

    @skip('Long scenario test only')
    @patch('sfctl.config.CLIConfig', new=MOCK_CLASS)
    def cluster_health_normal_test(self):
        """Get normal cluster health"""
        self.cmd('cluster health', checks=JMESPathCheck(
            'applicationHealthStates[0].name',
            'fabric:/System'
        ))
