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
    def cluster_select_no_security_test(self):
        """Select a cluster with no security"""
        self.cmd('cluster select --endpoint {0}'.format(ENDPOINT),
                 checks=[NoneCheck()])

    @skipUnless(ENDPOINT, 'Requires live cluster')
    @patch('sfctl.config.CLIConfig', new=MOCK_CONFIG)
    def cluster_health_normal_test(self):
        """Get normal cluster health"""
        self.cmd('cluster health', checks=[JMESPathCheck(
            'applicationHealthStates[0].name',
            'fabric:/System'
        )])
