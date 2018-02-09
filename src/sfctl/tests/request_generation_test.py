# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

#pylint: disable=line-too-long

"""Tests that the HTTP request generated is correct.
This requires a cluster connection."""

from __future__ import print_function
from unittest import skipUnless
from sys import (stderr, version_info)
from os import (remove, environ)
import json
import vcr
from mock import patch
from knack.testsdk import ScenarioTest
from jsonpickle import decode
from sfctl.entry import cli
from sfctl.tests.helpers import (MOCK_CONFIG, ENDPOINT)
from sfctl.tests.mock_server import (find_localhost_free_port, start_mock_server)
from sfctl.tests.request_generation_test_body_validation import validate_flat_dictionary # pylint: disable=line-too-long

python_version = version_info.major

class ServiceFabricRequestTests(ScenarioTest):
    """HTTP request generation tests for Service Fabric commands.
    This class requires a live connection to a cluster for some tests.
    This is so we generate commands in the way that the users will.
    The purpose of this test is to generate the commands and
    read the HTTP request to ensure correctness.
    The expected values are hard-coded.
    The VCR library records all HTTP requests into
    a file. For the sake of clarity,
    each test to write to its own file.
    The tests should then read the file to validate correctness.
    For on the fly debugging,
    printing to stdout does not print to the terminal/command line.
    Please use other output, such as stderr."""

    def __init__(self, method_name):
        cli_env = cli()
        super(ServiceFabricRequestTests, self).__init__(cli_env, method_name)

        # We do not want to run this suite of tests if python version is low.
        if python_version < 3:
            return

        # Save the value of SF_TEST_ENDPOINT set by the user
        self.old_enpoint = environ.get('SF_TEST_ENDPOINT', '')
        self.port = find_localhost_free_port()

    def __exit__(self, exception_type, exception_value, traceback):
        # Clean up the environment variables we changed during the test
        environ['SF_TEST_ENDPOINT'] = self.old_enpoint

    @patch('sfctl.config.CLIConfig', new=MOCK_CONFIG)
    def validate_command(self, command, method, path, query, body=None, #pylint: disable=too-many-locals,too-many-arguments
                         body_verifier=None):
        """
        This method takes the command passed in and runs the sfctl command.
        It records the input and output of the text file.
        It then validates the contexts of the text file against the provided
        expected results.
        All provided parameters other than self and command are expected values.

        Some considerations:
            - This test doesn't currently test for extra stuff, for example,
              no error will be returned if there is an extra parameter.
            - Ordering of the URI isn't enforced
              (path can appear before query for example)
            - API version is tested as a query parameter right now.
              Optimizations can be considered later.

        command (str): The command as it will appear in command line.
                For example, if a command if sfctl application list in
                command line, then use string 'application list'.
        method (str): The method of the HTTP request.
                Either GET, POST, or PUT
        body (str): The body as a string. Set value to None if
                no validation is required.
        body_verifier (function): A function which returns true if the passed
                in body passes validation. The method should take the
                command being run as a string (e.g. 'cluster report-health'),
                the actual, and the expected bodies as its inputs,
                in that order. The actual and expected bodies will be passed
                in as objects created by calling json.loads.
                Put None to skip this validation.
                If this is set to None but a body string is provided,
                validation will occur against the string as a string
                comparison.
        path (str): The section of the URI after host name and before the
                query portion. Do not include the port number.
        query (str list): A list of strings representing the query portion
                of the URI.
                Follows the format of ["parameter_name=parameter_value", ...].
                Make sure to include the API version of the HTTP request if
                required.
        """

        # For testing purposes, write to stderr with color
        print(file=stderr)
        print(command, file=stderr)

        generated_file_path = 'paths_generation_test.json'

        # In case this file was created and not deleted by a previous test,
        # delete it here
        try:
            remove(generated_file_path)
        except FileNotFoundError:
            # if the file doesn't exist, then there's nothing for us to do
            pass

        # This calls the command and the HTTP request is recorded into
        # generated_file_path
        with vcr.use_cassette('paths_generation_test.json',
                              record_mode='all', serializer='json'):
            self.cmd(command)

        # Read recorded JSON file
        with open(generated_file_path, 'r') as http_recording_file:
            json_str = http_recording_file.read()
            vcr_recording = decode(json_str)

            # The responses create an array of request and other objects.
            # the numbers (for indexing) represent which request was made
            # first.
            # the ordering is determined by the ordering of calls to self.cmd.
            # see outputted JSON file at generated_file_path for more details.
            recording = vcr_recording['interactions'][0]['request']

            # Validate method
            recording_method = recording['method']
            print('method: ' + recording_method, file=stderr)
            self.assertEqual(method, recording_method)

            # Validate body
            recording_body = recording['body']
            print('body: ' + str(recording_body), file=stderr)

            # body here is the expected body
            # recording_body is the actual value
            if body != None and body_verifier != None:
                actual_obj = json.loads(recording_body)
                expected_obj = json.loads(body)
                self.assertTrue(body_verifier(command, actual_obj,
                                              expected_obj))
            elif (body is not None) and (body_verifier is None):
                self.assertEqual(recording_body, body)

            # Get HTTP URI
            recording_uri = recording['uri']
            print('uri: ' + recording_uri, file=stderr)
            print('--- end cmd ' + command + ' ---', file=stderr)
            print(file=stderr)
            # An example URI
            # 'http://url:port/AppTypes/$/Provision?api-version=6.1'

            # Check that path is in recording_uri
            self.assertIn('http://localhost:' + str(self.port) + path,
                          recording_uri)

            # Check that the string appears in recording_uri
            for string in query:
                self.assertTrue((string + '&' in recording_uri) or
                                recording_uri.endswith(string))

        # If this test reaches here, then this test is successful.
        remove(generated_file_path) # Clean up

    def paths_generation_test(self):
        """ This test calls all commands that exist within sfctl.
        The commands are routed to a mock cluster which always returns
        success.We then read the values of the URL and other request
        features to determine that the command is working as expected
        (generating the correct URL). """

        # Set test URL path to that of our mock server
        environ['SF_TEST_ENDPOINT'] = 'http://localhost:' + str(self.port)
        # Start mock server
        start_mock_server(self.port)
        # Call test
        self.paths_generation_helper()
        # Reset test URL to user set value
        environ['SF_TEST_ENDPOINT'] = self.old_enpoint

    @skipUnless(ENDPOINT, 'Requires live cluster')
    @patch('sfctl.config.CLIConfig', new=MOCK_CONFIG)
    def provision_app_type_test(self): # pylint: disable=too-many-locals
        """Tests that a basic call to provision app type generates
        the correct HTTP request"""

        # We do not want to run this suite of tests if python version is low.
        if python_version < 3:
            return

        generated_file_path = 'HTTP_request_testing/provision_app_type.json'

        # To force new recordings, and to keep tests clean,
        # remove old test files
        try:
            remove(generated_file_path)
        except FileNotFoundError:
            # if the file doesn't exist, then there's nothing for us to do
            pass

        my_vcr = vcr.VCR(serializer='json', record_mode='all',
                         match_on=['uri', 'method'])

        # Record the HTTP request;
        # this writes the recordings to generated_file_path
        # Run async operation as false tests for simplicity
        with my_vcr.use_cassette(generated_file_path):
            try:
                self.cmd('application provision --image-store-provision \
                --application-type-build-path=test_path')
            except AssertionError:
                print('This does not indicate error. Caught exception. \
                    See {0} - first item - \
                    for details.'.format(generated_file_path), file=stderr)

            try:
                self.cmd('application provision --external-store-provision \
                    --application-package-download-uri=test_path \
                    --application-type-name=name \
                    --application-type-version=version')
            except AssertionError:
                print('This does not indicate an error. Caught exception. \
                    See {0} - second item - \
                    for details.'.format(generated_file_path), \
                      file=stderr)

        # Read recorded JSON file
        with open(generated_file_path, 'r') as http_recording_file:
            json_str = http_recording_file.read()
            vcr_recording = decode(json_str)

            # The responses create an array of request and other objects.
            # the numbers (for indexing) represent which request was made
            # first.
            # the ordering is determined by the ordering of calls to self.cmd.
            # see outputted JSON file at generated_file_path for more details.
            image_store_recording = vcr_recording['interactions'][0]['request']
            external_store_recording = \
                vcr_recording['interactions'][1]['request']

            # Get HTTP Body
            image_store_recording_body = decode(image_store_recording['body'])

            # Content inside HTTP body
            kind = image_store_recording_body['Kind']
            self.assertEqual(kind, 'ImageStorePath')

            async_operation = image_store_recording_body['Async']
            self.assertEqual(async_operation, False)

            application_type_build_path = \
                image_store_recording_body['ApplicationTypeBuildPath']
            self.assertEqual(application_type_build_path, 'test_path')

            # Get HTTP Body
            external_store_recording_body = \
                decode(external_store_recording['body'])

            # Content inside HTTP body
            kind = external_store_recording_body['Kind']
            self.assertEqual(kind, 'ExternalStore')

            async_operation = external_store_recording_body['Async']
            self.assertEqual(async_operation, False)

            download_uri = \
                external_store_recording_body['ApplicationPackageDownloadUri']
            self.assertEqual(download_uri, 'test_path')

            application_type_name = \
                external_store_recording_body['ApplicationTypeName']
            self.assertEqual(application_type_name, 'name')

            application_type_version = \
                external_store_recording_body['ApplicationTypeVersion']
            self.assertEqual(application_type_version, 'version')

            # Get HTTP Method type (Get vs Post)
            image_store_recording_method = image_store_recording['method']
            self.assertEqual(image_store_recording_method, 'POST')

            external_store_recording_method = \
                external_store_recording['method']
            self.assertEqual(external_store_recording_method, 'POST')

            # Get HTTP URI
            image_store_recording_uri = image_store_recording['uri']
            # assert
            # '/ApplicationTypes/$/Provision?api-version=6.1&timeout=60'
            # in image_store_recording_uri
            self.assertIn(
                '/ApplicationTypes/$/Provision?api-version=6.1&timeout=60',
                image_store_recording_uri)

            external_store_recording_uri = external_store_recording['uri']
            self.assertIn(
                '/ApplicationTypes/$/Provision?api-version=6.1&timeout=60',
                external_store_recording_uri)

        # If this test reaches here, then this test is successful.

    def paths_generation_helper(self): # pylint: disable=too-many-statements
        """ Lists all the commands to be tested and their expected values.
        Expected values here refer to the expected URI that is generated
        and sent to the cluster."""

        # Cluster commands:
        # Select command tested elsewhere.
        # Cluster upgrade and upgrade-update test to be added later
        self.validate_command( # code-versions
            'sfctl cluster code-versions --code-version=version',
            'GET',
            '/$/GetProvisionedCodeVersions',
            ['api-version=6.0', 'CodeVersion=version'])
        self.validate_command( # config-versions
            'sfctl cluster config-versions --config-version=version',
            'GET',
            '/$/GetProvisionedConfigVersions',
            ['api-version=6.0', 'ConfigVersion=version'])
        self.validate_command( # health - Use exclude-health-statistics param
            'sfctl cluster health --applications-health-state-filter=2 \
                --events-health-state-filter=2 --exclude-health-statistics \
                --nodes-health-state-filter=2',
            'GET',
            '/$/GetClusterHealth',
            ['api-version=6.0',
             'NodesHealthStateFilter=2',
             'ApplicationsHealthStateFilter=2',
             'EventsHealthStateFilter=2',
             'ExcludeHealthStatistics=true'])
        # Use include-system-application-health-statistics param
        self.validate_command( # health
            'sfctl cluster health --applications-health-state-filter=2 \
                --events-health-state-filter=2 \
                --include-system-application-health-statistics \
                --nodes-health-state-filter=2',
            'GET',
            '/$/GetClusterHealth',
            ['api-version=6.0',
             'NodesHealthStateFilter=2',
             'ApplicationsHealthStateFilter=2',
             'EventsHealthStateFilter=2',
             'IncludeSystemApplicationHealthStatistics=true'])
        self.validate_command( # manifest
            'sfctl cluster manifest',
            'GET',
            '/$/GetClusterManifest',
            ['api-version=6.0'])
        self.validate_command( # provision
            'sfctl cluster provision --cluster-manifest-file-path=value --code-file-path=value2',
            'POST',
            '/$/Provision',
            ['api-version=6.0'],
            '{"CodeFilePath":"value2","ClusterManifestFilePath":"value"}',
            validate_flat_dictionary)
        # "P3Y6M4DT12H30M5S" represents a duration of "three years,
        # six months, four days, twelve hours, thirty minutes,
        # and five seconds".
        self.validate_command( # report-health
            'sfctl cluster report-health --immediate --source-id=ID' +
            ' --health-property=Property ' +
            '--health-state=Warning --ttl=P3Y6M4DT12H30M5S ' +
            '--description=Description ' +
            '--sequence-number=10 --remove-when-expired',
            'POST',
            '/$/ReportClusterHealth',
            ['api-version=6.0', 'Immediate=true'],
            '{"SourceId": "ID", \
                "Property": "Property", \
                "HealthState": "Warning", \
                "TimeToLiveInMilliSeconds": "P3Y6M4DT12H30M5S", \
                "Description": "Description", \
                "SequenceNumber": "10", \
                "RemoveWhenExpired": true}',
            validate_flat_dictionary)
        self.validate_command( # unprovision
            'sfctl cluster unprovision --code-version=code --config-version=config',
            'POST',
            '/$/Unprovision',
            ['api-version=6.0'],
            '{"CodeVersion":"code","ConfigVersion":"config"}',
            validate_flat_dictionary)
        self.validate_command( # upgrade-resume
            'sfctl cluster upgrade-resume --upgrade-domain=UD2',
            'POST',
            '/$/MoveToNextUpgradeDomain',
            ['api-version=6.0'],
            '{"UpgradeDomain":"UD2"}',
            validate_flat_dictionary)
        self.validate_command( # upgrade-rollback
            'sfctl cluster upgrade-rollback',
            'POST',
            '/$/RollbackUpgrade',
            ['api-version=6.0'])
        self.validate_command( # upgrade-status
            'sfctl cluster upgrade-status',
            'GET',
            '/$/GetUpgradeProgress',
            ['api-version=6.0'])

        # Node Commands:
        self.validate_command( # disable
            'sfctl node disable --node-name=nodeName --deactivation-intent=Pause',
            'POST',
            '/Nodes/nodeName/$/Deactivate',
            ['api-version=6.0'],
            '{"DeactivationIntent":"Pause"}',
            validate_flat_dictionary)
        self.validate_command( # enable
            'sfctl node enable --node-name=nodeName',
            'POST',
            '/Nodes/nodeName/$/Activate',
            ['api-version=6.0'])
        self.validate_command( # health
            'sfctl node health --node-name=nodeName --events-health-state-filter=2',
            'GET',
            '/Nodes/nodeName/$/GetHealth',
            ['api-version=6.0', 'EventsHealthStateFilter=2'])
        self.validate_command( # info
            'sfctl node info --node-name=nodeName',
            'GET',
            '/Nodes/nodeName',
            ['api-version=6.0'])
        self.validate_command( # list
            'sfctl node list --continuation-token=nodeId --node-status-filter=up',
            'GET',
            '/Nodes',
            ['api-version=6.0', 'ContinuationToken=nodeId', 'NodeStatusFilter=up'])
        self.validate_command( # load
            'sfctl node load --node-name=nodeName',
            'GET',
            '/Nodes/nodeName/$/GetLoadInformation',
            ['api-version=6.0'])
        self.validate_command( # remove-state
            'sfctl node remove-state --node-name=nodeName',
            'POST',
            '/Nodes/nodeName/$/RemoveNodeState',
            ['api-version=6.0'])
        self.validate_command( # report-health
            'sfctl node report-health --node-name=nodeName --immediate --source-id=ID --health-property=Property ' +
            '--health-state=Warning --ttl=P3Y6M4DT12H30M5S --description=Description ' +
            '--sequence-number=10 --remove-when-expired=true',
            'POST',
            '/Nodes/nodeName/$/ReportHealth',
            ['api-version=6.0', 'Immediate=true'],
            '{"SourceId": "ID", \
                "Property": "Property", \
                "HealthState": "Warning", \
                "TimeToLiveInMilliSeconds": "P3Y6M4DT12H30M5S", \
                "Description": "Description", \
                "SequenceNumber": "10", \
                "RemoveWhenExpired": true}',
            validate_flat_dictionary)
        self.validate_command( # restart
            'sfctl node restart --node-name=nodeName --node-instance-id=ID --create-fabric-dump=True',
            'POST',
            '/Nodes/nodeName/$/Restart',
            ['api-version=6.0'],
            '{"CreateFabricDump":"True", "NodeInstanceId":"ID"}',
            validate_flat_dictionary)

        # Application Commands:
        # Application create tests not yet added
        # Application upgrade is not tested for all parameters
        # application upload tested as part of a custom command
        self.validate_command( # delete
            'application delete --application-id=application~Id --force-remove=true',
            'POST',
            '/Applications/application~Id/$/Delete',
            ['api-version=6.0', 'ForceRemove=true'])
        self.validate_command( # deployed
            'application deployed --application-id=application~Id --node-name=nodeName --include-health-state',
            'GET',
            '/Nodes/nodeName/$/GetApplications/application~Id',
            ['api-version=6.1', 'IncludeHealthState=true'])
        self.validate_command( # deployed-list
            'application deployed-list --node-name=nodeName --continuation-token=token --include-health-state --max-results=10',
            'GET',
            '/Nodes/nodeName/$/GetApplications',
            ['api-version=6.1', 'ContinuationToken=token', 'IncludeHealthState=true', 'MaxResults=10'])
        self.validate_command( # deployed-health
            'application deployed-health --node-name=nodeName --application-id=app~id --deployed-service-packages-health-state-filter=2 ' +
            '--events-health-state-filter=2 --exclude-health-statistics',
            'GET',
            '/Nodes/nodeName/$/GetApplications/app~id/$/GetHealth',
            ['api-version=6.0', 'EventsHealthStateFilter=2', 'ExcludeHealthStatistics=true', 'DeployedServicePackagesHealthStateFilter=2'])
        self.validate_command( # health
            'application health --application-id=app~id --deployed-applications-health-state-filter=2 --services-health-state-filter=2 ' +
            '--events-health-state-filter=2 --exclude-health-statistics',
            'GET',
            '/Applications/app~id/$/GetHealth',
            ['api-version=6.0', 'EventsHealthStateFilter=2', 'ExcludeHealthStatistics=true', 'DeployedApplicationsHealthStateFilter=2',
             'ServicesHealthStateFilter=2'])
        self.validate_command( # info
            'application info --application-id=application~Id --exclude-application-parameters',
            'GET',
            '/Applications/application~Id',
            ['api-version=6.0', 'ExcludeApplicationParameters=true'])
        self.validate_command( # list
            'application list --application-type-name=name --continuation-token=token --exclude-application-parameters --max-results=10',
            'GET',
            '/Applications',
            ['api-version=6.1', 'ContinuationToken=token', 'ExcludeApplicationParameters=true', 'MaxResults=10', 'ApplicationTypeName=name'])
        self.validate_command( # load
            'application load --application-id=application~Id',
            'GET',
            '/Applications/application~Id/$/GetLoadInformation',
            ['api-version=6.0'])
        self.validate_command( # report-health
            'application report-health --application-id=id --immediate --source-id=ID --health-property=Property ' +
            '--health-state=Warning --ttl=P3Y6M4DT12H30M5S --description=Description ' +
            '--sequence-number=10 --remove-when-expired=true',
            'POST',
            '/Applications/id/$/ReportHealth',
            ['api-version=6.0', 'Immediate=true'],
            '{"SourceId": "ID", \
                "Property": "Property", \
                "HealthState": "Warning", \
                "TimeToLiveInMilliSeconds": "P3Y6M4DT12H30M5S", \
                "Description": "Description", \
                "SequenceNumber": "10", \
                "RemoveWhenExpired": true}',
            validate_flat_dictionary)

        # Ask area owner to fill out this test
        # self.validate_command( # upgrade - not all parameters tested
        #    'application upgrade --application-name=name --application-version=version --parameters={} ' +
        #    '--failure-action=Rollback',
        #    'POST',
        #    '/Applications/name/$/Upgrade',
        #    ['api-version=6.0'])

        self.validate_command( # upgrade-resume
            'application upgrade-resume --application-id=application~Id --upgrade-domain-name=UD2',
            'POST',
            '/Applications/application~Id/$/MoveToNextUpgradeDomain',
            ['api-version=6.0'],
            '{"UpgradeDomainName":"UD2"}',
            validate_flat_dictionary)
        self.validate_command( # upgrade-rollback
            'application upgrade-rollback --application-id=application~Id',
            'POST',
            '/Applications/application~Id/$/RollbackUpgrade',
            ['api-version=6.0'])
        self.validate_command( # upgrade-status
            'application upgrade-status --application-id=application~Id',
            'GET',
            '/Applications/application~Id/$/GetUpgradeProgress',
            ['api-version=6.0'])

        # Compose
        # create is not tested here because it requires reading in a file.
        self.validate_command( # list
            'compose list --continuation-token=token --max-results=10',
            'GET',
            '/ComposeDeployments',
            ['api-version=6.0-preview', 'ContinuationToken=token', 'MaxResults=10'])
        self.validate_command( # status
            'compose status --deployment-name=deploymentName',
            'GET',
            '/ComposeDeployments/deploymentName',
            ['api-version=6.0-preview'])
        self.validate_command( # remove
            'compose remove --deployment-name=deploymentName',
            'POST',
            '/ComposeDeployments/deploymentName/$/Delete',
            ['api-version=6.0-preview'])
        self.validate_command( # upgrade-status
            'compose upgrade-status --deployment-name=deploymentName',
            'GET',
            '/ComposeDeployments/deploymentName/$/GetUpgradeProgress',
            ['api-version=6.0-preview'])

        # IS:
        self.validate_command( # command
            'is command --command=cmd --service-id=id',
            'POST',
            '/$/InvokeInfrastructureCommand',
            ['api-version=6.0', 'Command=cmd', 'ServiceId=id'])
        self.validate_command( # query
            'is query --command=cmd --service-id=id',
            'GET',
            '/$/InvokeInfrastructureQuery',
            ['api-version=6.0', 'Command=cmd', 'ServiceId=id'])

        # Partition
        self.validate_command( # health
            'partition health --partition-id=id --events-health-state-filter=2 --exclude-health-statistics --replicas-health-state-filter=2',
            'GET',
            '/Partitions/id/$/GetHealth',
            ['api-version=6.0', 'EventsHealthStateFilter=2', 'ReplicasHealthStateFilter=2', 'ExcludeHealthStatistics=true'])
        self.validate_command( # info
            'partition info --partition-id=id',
            'GET',
            '/Partitions/id',
            ['api-version=6.0'])
        self.validate_command( # list
            'partition list --service-id=fabric:/app/id --continuation-token=ct',
            'GET',
            '/Services/fabric:/app/id/$/GetPartitions',
            ['api-version=6.0', 'ContinuationToken=ct'])
        self.validate_command( # load
            'partition load --partition-id=id',
            'GET',
            '/Partitions/id/$/GetLoadInformation',
            ['api-version=6.0'])
        self.validate_command( # load-reset
            'partition load-reset --partition-id=id',
            'POST',
            '/Partitions/id/$/ResetLoad',
            ['api-version=6.0'])
        self.validate_command( # recover
            'partition recover --partition-id=id',
            'POST',
            '/Partitions/id/$/Recover',
            ['api-version=6.0'])
        self.validate_command( # recover-all
            'partition recover-all',
            'POST',
            '/$/RecoverAllPartitions',
            ['api-version=6.0'])
        self.validate_command( # svc-name
            'partition svc-name --partition-id=id',
            'GET',
            '/Partitions/id/$/GetServiceName',
            ['api-version=6.0'])
        self.validate_command( # report-health
            'partition report-health --partition-id=id --immediate --source-id=ID --health-property=Property ' +
            '--health-state=Warning --ttl=P3Y6M4DT12H30M5S --description=Description ' +
            '--sequence-number=10 --remove-when-expired=true',
            'POST',
            '/Partitions/id/$/ReportHealth',
            ['api-version=6.0', 'Immediate=true'],
            '{"SourceId": "ID", \
                "Property": "Property", \
                "HealthState": "Warning", \
                "TimeToLiveInMilliSeconds": "P3Y6M4DT12H30M5S", \
                "Description": "Description", \
                "SequenceNumber": "10", \
                "RemoveWhenExpired": true}',
            validate_flat_dictionary)

        # Property
        value = '"{\\"Kind\\": \\"String\\", \\"Data\\": \\"data\\"}"'
        self.validate_command( # put
            'property put --name-id=name --property-name=property --custom-id-type=type --value=' + value,
            'PUT',
            '/Names/name/$/GetProperty',
            ['api-version=6.0'],
            '{"PropertyName":"property", "CustomTypeId":"type", "Value":{"Kind": "String", "Data": "data"}}',
            validate_flat_dictionary)
        self.validate_command( # get
            'property get --name-id=name --property-name=property',
            'GET',
            '/Names/name/$/GetProperty',
            ['api-version=6.0', 'PropertyName=property'])
        self.validate_command( # list
            'property list --name-id=name --continuation-token=ct --include-values',
            'GET',
            '/Names/name/$/GetProperties',
            ['api-version=6.0', 'IncludeValues=true', 'ContinuationToken=ct'])
        self.validate_command( # delete
            'property delete --name-id=name --property-name=property',
            'DELETE',
            '/Names/name/$/GetProperty',
            ['api-version=6.0', 'PropertyName=property'])

        # Replica
        self.validate_command( # deployed
            'replica deployed --node-name=nodeName --partition-id=id --replica-id=replicaId',
            'GET',
            '/Nodes/nodeName/$/GetPartitions/id/$/GetReplicas/replicaId/$/GetDetail',
            ['api-version=6.0'])
        self.validate_command( # deployed-list
            'replica deployed-list --node-name=nodeName --partition-id=id --application-id=applicationId --service-manifest-name=serviceManifestName',
            'GET',
            '/Nodes/nodeName/$/GetApplications/applicationId/$/GetReplicas',
            ['api-version=6.0', 'PartitionId=id', 'ServiceManifestName=serviceManifestName'])
        self.validate_command( # health
            'replica health --events-health-state-filter=2 --partition-id=id --replica-id=replicaId',
            'GET',
            '/Partitions/id/$/GetReplicas/replicaId/$/GetHealth',
            ['api-version=6.0', 'EventsHealthStateFilter=2'])
        self.validate_command( # info
            'replica info --continuation-token=ct --partition-id=id --replica-id=replicaId',
            'GET',
            '/Partitions/id/$/GetReplicas/replicaId',
            ['api-version=6.0', 'ContinuationToken=ct'])
        self.validate_command( # list
            'replica list --continuation-token=ct --partition-id=id',
            'GET',
            '/Partitions/id/$/GetReplicas',
            ['api-version=6.0', 'ContinuationToken=ct'])
        self.validate_command( # remove
            'replica remove --node-name=nodeName --partition-id=id --replica-id=replicaId --force-remove=true',
            'POST',
            '/Nodes/nodeName/$/GetPartitions/id/$/GetReplicas/replicaId/$/Delete',
            ['api-version=6.0', 'ForceRemove=true'])
        self.validate_command( # report-health
            'replica report-health --partition-id=id --replica-id=replicaId --service-kind=Stateless --immediate --source-id=ID --health-property=Property ' +
            '--health-state=Warning --ttl=P3Y6M4DT12H30M5S --description=Description ' +
            '--sequence-number=10 --remove-when-expired=true',
            'POST',
            '/Partitions/id/$/GetReplicas/replicaId/$/ReportHealth',
            ['api-version=6.0', 'Immediate=true', 'ServiceKind=Stateless'],
            '{"SourceId": "ID", \
                "Property": "Property", \
                "HealthState": "Warning", \
                "TimeToLiveInMilliSeconds": "P3Y6M4DT12H30M5S", \
                "Description": "Description", \
                "SequenceNumber": "10", \
                "RemoveWhenExpired": true}',
            validate_flat_dictionary)
        self.validate_command( # restart
            'replica restart --node-name=nodeName --partition-id=id --replica-id=replicaId',
            'POST',
            '/Nodes/nodeName/$/GetPartitions/id/$/GetReplicas/replicaId/$/Restart',
            ['api-version=6.0'])

        # RPM
        self.validate_command( # approve-force
            'rpm approve-force --task-id=id --version=version',
            'POST',
            '/$/ForceApproveRepairTask',
            ['api-version=6.0'],
            '{"TaskId":"id", "Version":"version"}',
            validate_flat_dictionary)
        self.validate_command( # delete
            'rpm delete --task-id=id --version=version',
            'POST',
            '/$/DeleteRepairTask',
            ['api-version=6.0'],
            '{"TaskId":"id", "Version":"version"}',
            validate_flat_dictionary)
        self.validate_command( # list
            'rpm list --executor-filter=ex --state-filter=2 --task-id-filter=task',
            'GET',
            '/$/GetRepairTaskList',
            ['api-version=6.0', 'TaskIdFilter=task', 'StateFilter=2', 'ExecutorFilter=ex'])

        # Store
        self.validate_command( # delete
            'store delete --content-path=path',
            'DELETE',
            '/ImageStore/path',
            ['api-version=6.0'])
        self.validate_command( # root-info
            'store root-info',
            'GET',
            '/ImageStore',
            ['api-version=6.0'])
        self.validate_command( # stat
            'store stat --content-path=path',
            'GET',
            '/ImageStore/path',
            ['api-version=6.0'])

        # Service
        # create and update tests not added for now
        self.validate_command( # app-name
            'service app-name --service-id=some~service~path',
            'GET',
            '/Services/some~service~path/$/GetApplicationName',
            ['api-version=6.0'])
        self.validate_command( # delete
            'service delete --service-id=some~service~path --force-remove=true',
            'POST',
            '/Services/some~service~path/$/Delete',
            ['api-version=6.0', 'ForceRemove=true'])
        self.validate_command( # description
            'service description --service-id=some~service~path',
            'GET',
            '/Services/some~service~path/$/GetDescription',
            ['api-version=6.0'])
        self.validate_command( # health
            'service health --service-id=some~service~path --events-health-state-filter=2 --exclude-health-statistics --partitions-health-state-filter=2',
            'GET',
            '/Services/some~service~path/$/GetHealth',
            ['api-version=6.0', 'EventsHealthStateFilter=2', 'PartitionsHealthStateFilter=2', 'ExcludeHealthStatistics=true'])
        self.validate_command( # info
            'service info --service-id=some~service~path --application-id=app~id',
            'GET',
            '/Applications/app~id/$/GetServices/some~service~path',
            ['api-version=6.0'])
        self.validate_command( # list
            'service list --service-type-name=type --application-id=app~id --continuation-token=ct',
            'GET',
            '/Applications/app~id/$/GetServices',
            ['api-version=6.0', 'ServiceTypeName=type', 'ContinuationToken=ct'])
        self.validate_command( # resolve
            'service resolve --service-id=some~service~path --partition-key-type=3 --partition-key-value=part --previous-rsp-version=version',
            'GET',
            '/Services/some~service~path/$/ResolvePartition',
            ['api-version=6.0', 'PartitionKeyType=3', 'PartitionKeyValue=part', 'PreviousRspVersion=version'])
        self.validate_command( # report-health
            'service report-health --service-id=service~id --immediate --source-id=ID --health-property=Property ' +
            '--health-state=Warning --ttl=P3Y6M4DT12H30M5S --description=Description ' +
            '--sequence-number=10 --remove-when-expired=true',
            'POST',
            '/Services/service~id/$/ReportHealth',
            ['api-version=6.0', 'Immediate=true'],
            '{"SourceId": "ID", \
                "Property": "Property", \
                "HealthState": "Warning", \
                "TimeToLiveInMilliSeconds": "P3Y6M4DT12H30M5S", \
                "Description": "Description", \
                "SequenceNumber": "10", \
                "RemoveWhenExpired": true}',
            validate_flat_dictionary)
