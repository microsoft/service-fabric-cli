# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Live scenario tests that cannot be recorded for Service Fabric commands"""

import os
from unittest import skipUnless
from mock import patch
from knack.testsdk import (ScenarioTest, NoneCheck, JMESPathCheckExists)
from knack.testsdk.decorators import live_only
from sfctl.entry import cli
from sfctl.tests.helpers import (APP_PATH, ENDPOINT, MOCK_CONFIG,
                                 parse_app_version, parse_app_type,
                                 parse_service_type, find_service_manifest)


class ServiceFabricLiveTests(ScenarioTest):
    """Live scenario tests for Service Fabric commands"""

    def __init__(self, method_name):
        cli_env = cli()
        super(ServiceFabricLiveTests, self).__init__(cli_env, method_name)

    @skipUnless(ENDPOINT and APP_PATH,
                'Requires live cluster and test application')
    @patch('sfctl.config.CLIConfig', new=MOCK_CONFIG)
    @live_only()
    def test_application_lifecycle(self):
        """Attempt to perform all operations in an application lifecycle
        excluding upgrade

        An application lifecycle has the following steps:
        - Upload, application package is copied to the Service Fabric
          image store
        - Provision, application is provisioned
        - Create, application becomes instantiated
        - Service create, services are created from an application,
        - Delete, application instance is deleted,
        - Unprovision, application is unprovisioned
        - Package delete, application package is removed from image store
        """

        # Upload application
        if not os.path.isdir(APP_PATH):
            raise ValueError(
                'Invalid path to application specified: {0}'.format(APP_PATH)
            )
        folder_name = os.path.basename(os.path.dirname(APP_PATH))
        app_manifest = os.path.join(APP_PATH, 'ApplicationManifest.xml')
        app_ver = parse_app_version(app_manifest)
        app_type = parse_app_type(app_manifest)
        upload_cmd = 'application upload --path {0} --show-progress'
        self.cmd(upload_cmd.format(APP_PATH), checks=[NoneCheck()])

        # Validate folder exists by stating the path
        root_info_check = (
            'storeFolders[?storeRelativePath==\'{0}\']'.format(folder_name)
        )
        self.cmd('store root-info',
                 checks=[JMESPathCheckExists(root_info_check)])

        # Provision application
        provision_cmd = ('application provision --application-type-build-path '
                         '{0}')
        self.cmd(provision_cmd.format(folder_name), checks=[NoneCheck()])

        # Validate provision
        provision_check = (
            'items[?name==\'{0}\'&&version==\'{1}\']'.format(app_type, app_ver)
        )
        self.cmd('application type-list', checks=[JMESPathCheckExists(
            provision_check
        )])

        # Create application
        create_cmd = ('application create --app-name {0} --app-type {1} '
                      '--app-version {2}')
        self.cmd(create_cmd.format('fabric:/test', app_type, app_ver),
                 checks=[NoneCheck()])

        # Validate create
        self.cmd('application list', checks=JMESPathCheckExists(
            'items[?name==\'fabric:/test\']'
        ))

        # Service create
        st_kind, st_name = parse_service_type(
            find_service_manifest(app_manifest)
        )
        if st_kind != 'stateless':
            raise ValueError('Unsupported service type')
        create_svc_cmd = ('service create --app-id test '
                          '--name fabric:/test/testsvc '
                          '--service-type {0} --stateless '
                          '--singleton-scheme --instance-count 1')
        self.cmd(create_svc_cmd.format(st_name), checks=[NoneCheck()])

        # Validate service create
        self.cmd('service list --application-id test',
                 checks=[JMESPathCheckExists(
                     'items[?name==\'fabric:/test/testsvc\']'
                 )])

        # Delete application
        self.cmd('application delete --application-id test',
                 checks=[NoneCheck()])

        # Unprovision application
        # Remove expect_failure once issue #6 fixed
        unprovision_cmd = ('application unprovision --application-type-name '
                           '{0} --application-type-version {1}')
        self.cmd(unprovision_cmd.format(app_type, app_ver),
                 expect_failure=True)

        # Delete application package folder
        self.cmd('store delete --content-path {0}'.format(folder_name),
                 checks=[NoneCheck()])
