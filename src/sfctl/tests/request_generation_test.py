# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

# pylint: disable=line-too-long

"""Tests that the HTTP request generated is correct.
This does not require a cluster connection, except the test for provision application type."""

from __future__ import print_function
from os import (remove, environ, path)
import json
import logging
import vcr
from mock import patch
from knack.testsdk import ScenarioTest
from jsonpickle import decode
from sfctl.entry import cli
from sfctl.tests.helpers import MOCK_CONFIG
from sfctl.tests.mock_server import (find_localhost_free_port, start_mock_server)
from sfctl.tests.request_generation_body_validation import validate_flat_dictionary


class ServiceFabricRequestTests(ScenarioTest):
    """HTTP request generation tests for Service Fabric commands.
    This class requires a live connection to a cluster for some tests.
    This is so we generate commands in the way that the users will.
    The purpose of this test is to generate the commands and
    read the HTTP request to ensure correctness. The expected values are hard-coded.
    The VCR library records all HTTP requests into
    a file. For the sake of clarity, each test writes to its own file.
    The tests should then read the file to validate correctness. For on the fly debugging,
    printing to stdout does not print to the terminal/command line.
    Please use other outputs, such as stderr."""

    def __init__(self, method_name):
        cli_env = cli()
        super(ServiceFabricRequestTests, self).__init__(cli_env, method_name)

        # Save the value of SF_TEST_ENDPOINT set by the user
        self.old_endpoint = environ.get('SF_TEST_ENDPOINT', '')
        self.port = find_localhost_free_port()

        # Start mock server
        start_mock_server(self.port)

    def __exit__(self, exception_type, exception_value, traceback):
        # Revert the environment variables we changed during the test to what the user set.
        environ['SF_TEST_ENDPOINT'] = self.old_endpoint

    @patch('sfctl.config.CLIConfig', new=MOCK_CONFIG)
    def validate_command(self, command, method, url_path, query, body=None,  # pylint: disable=too-many-locals, too-many-arguments
                         body_verifier=None):
        """
        This method takes the command passed in and runs the sfctl command specified.
        It records the input and output in a text file. It then validates the contexts of
        the text file against the provided expected results.
        All provided parameters other than self and command are expected values, rather than
        actual values by running the sfctl command.

        Some considerations:
            - This test doesn't currently test for things like different combinations of
              input parameters.
            - Ordering of the URI isn't enforced
              (path can appear before query for example)
            - API version is tested as a query parameter right now.
              Optimizations can be considered later.

        command (str): The command as it will appear in command line.
                For example, if a command if sfctl application list in
                command line, then use string 'application list'.
        method (str): The method of the HTTP request.
                For example, GET, POST, PUT, etc.
        body (str): The body as a string. Set value to None if
                no validation is required. What format this string should be in
                depends on the body_verifier function which is passed in. If a
                function is not passed, but this value is not None, then a simple
                string comparison will be done.
        body_verifier (function): A function which returns true if the passed
                in body (str) passes validation. The method should take:
                    1. Command being run as a string (e.g. 'cluster report-health'),
                    2. Actual, and the expected bodies as its inputs, in that order.
                       The actual and expected bodies will be passed in as objects
                       created by calling json.loads.
                Put None to skip this validation.
                If this is set to None but a body string is provided,
                validation will occur against the string as a string
                comparison.
        path (str): The section of the URI after host name and before the
                query portion. Do not include the port number.
        query (str list): A list of strings representing the query portion
                of the URI. Follows the format of ["parameter_name=parameter_value", ...].
                Make sure to include the API version of the HTTP request if
                required.
        """

        # For testing purposes, write to stderr with color

        generated_file_path = 'paths_generation_test.json'

        # In case this file was created and not deleted by a previous test,
        # delete it here
        try:
            remove(generated_file_path)
        except OSError:
            # if the file doesn't exist, then there's nothing for us to do here
            pass

        # This calls the command and the HTTP request it recorded into
        # generated_file_path

        # Reduce noise in test output for this test only
        logging.disable(logging.INFO)
        with vcr.use_cassette('paths_generation_test.json', record_mode='all', serializer='json'):
            try:
                self.cmd(command)
            except Exception as exception:  # pylint: disable=broad-except
                self.fail('ERROR while running command "{0}". Error: "{1}"'.format(command, str(exception)))

        # re-enable logging
        logging.disable(logging.NOTSET)

        # Read recorded JSON file
        with open(generated_file_path, 'r') as http_recording_file:
            json_str = http_recording_file.read()
            vcr_recording = decode(json_str)

            # The responses create an array of request and other objects.
            # the numbers (for indexing) represent which request was made
            # first. The ordering is determined by the ordering of calls to self.cmd.
            # see outputted JSON file at generated_file_path for more details.
            recording = vcr_recording['interactions'][0]['request']

            # Validate method (GET, POST, etc)
            recording_method = recording['method']

            self.assertEqual(method, recording_method,
                             msg='Method mismatch. Expected {0}. Got {1}'.format(recording_method, method))

            # Validate body
            recording_body = recording['body']

            # body here is the expected body
            # recording_body is the actual value
            if body is not None and body_verifier is not None:
                actual_obj = json.loads(recording_body)
                expected_obj = json.loads(body)
                self.assertTrue(body_verifier(command, actual_obj, expected_obj),
                                msg='body_verifier command failed. The command should either print error'
                                    'messages, or call its own asserts.')
            elif (body is not None) and (body_verifier is None):
                self.assertEqual(recording_body, body,
                                 msg='Performing a string comparison for body.'
                                     'Expected "{0}". Got "{1}"'.format(recording_body, body))

            # Get HTTP URI
            recording_uri = recording['uri']
            # An example URI
            # 'http://url:port/AppTypes/$/Provision?api-version=6.1'

            # Check that path is in recording_uri
            uri_path_start = 'http://localhost:' + str(self.port) + url_path
            self.assertIn(uri_path_start, recording_uri,
                          msg='Uri starting portion "{0}" was not found in generated URI "{1}"'.format(uri_path_start, recording_uri))

            # Check that the string appears in recording_uri
            for string in query:
                self.assertTrue((string in recording_uri),
                                msg='"{0}" not found in URI query section "{1}"'.format(string, recording_uri))

        # If this test reaches here, then this test is successful.
        remove(generated_file_path)  # Clean up

    def test_paths_generation(self):
        """ This test calls all commands that exist within sfctl.
        The commands are routed to a mock cluster which always returns
        success.We then read the values of the URL and other request
        features to determine that the command is working as expected
        (generating the correct URL). """

        # Set test URL path to that of our mock server
        environ['SF_TEST_ENDPOINT'] = 'http://localhost:' + str(self.port)

        # Call test
        self.paths_generation_helper()

    def paths_generation_helper(self):  # pylint: disable=too-many-statements
        """ Lists all the commands to be tested and their expected values.
        Expected values here refer to the expected URI that is generated
        and sent to the cluster."""

        sample_path_base = '@' + path.join(path.dirname(__file__), 'sample_json')

        # Application Type Commands
        self.validate_command(  # provision-application-type image-store
            'application provision --application-type-build-path=test_path',
            'POST',
            '/ApplicationTypes/$/Provision',
            ['api-version=6.2', 'timeout=60'],
            ('{"Kind": "ImageStorePath", '
             '"Async": false, '
             '"ApplicationTypeBuildPath": "test_path"}'),
            validate_flat_dictionary)

        self.validate_command(  # provision-application-type external-store
            'application provision --external-provision '
            '--application-package-download-uri=test_path --application-type-name=name '
            '--application-type-version=version',
            'POST',
            '/ApplicationTypes/$/Provision',
            ['api-version=6.2', 'timeout=60'],
            ('{"Kind": "ExternalStore", '
             '"Async": false, '
             '"ApplicationPackageDownloadUri": "test_path", '
             '"ApplicationTypeName": "name", '
             '"ApplicationTypeVersion": "version"}'),
            validate_flat_dictionary)

        # Cluster commands:
        # Select command tested elsewhere.
        # Cluster upgrade and upgrade-update test to be added later
        self.validate_command(   # config-versions
            'sfctl cluster config-versions --config-version=version',
            'GET',
            '/$/GetProvisionedConfigVersions',
            ['api-version=6.0', 'ConfigVersion=version'])
        self.validate_command(  # health - Use exclude-health-statistics param
            'sfctl cluster health --applications-health-state-filter=2 '
            '--events-health-state-filter=2 --exclude-health-statistics '
            '--nodes-health-state-filter=2',
            'GET',
            '/$/GetClusterHealth',
            ['api-version=6.0',
             'NodesHealthStateFilter=2',
             'ApplicationsHealthStateFilter=2',
             'EventsHealthStateFilter=2',
             'ExcludeHealthStatistics=true'])
        # Use include-system-application-health-statistics param
        self.validate_command(  # health
            'sfctl cluster health --applications-health-state-filter=2 '
            '--events-health-state-filter=2 '
            '--include-system-application-health-statistics '
            '--nodes-health-state-filter=2',
            'GET',
            '/$/GetClusterHealth',
            ['api-version=6.0',
             'NodesHealthStateFilter=2',
             'ApplicationsHealthStateFilter=2',
             'EventsHealthStateFilter=2',
             'IncludeSystemApplicationHealthStatistics=true'])
        self.validate_command(  # manifest
            'sfctl cluster manifest',
            'GET',
            '/$/GetClusterManifest',
            ['api-version=6.0'])
        self.validate_command(  # provision
            'sfctl cluster provision --cluster-manifest-file-path=value --code-file-path=value2',
            'POST',
            '/$/Provision',
            ['api-version=6.0'],
            '{"CodeFilePath":"value2","ClusterManifestFilePath":"value"}',
            validate_flat_dictionary)
        # "P3Y6M4DT12H30M5S" represents a duration of "three years,
        # six months, four days, twelve hours, thirty minutes,
        # and five seconds".
        self.validate_command(  # report-health
            'sfctl cluster report-health --immediate --source-id=ID' +
            ' --health-property=Property ' +
            '--health-state=Warning --ttl=P3Y6M4DT12H30M5S ' +
            '--description=Description ' +
            '--sequence-number=10 --remove-when-expired',
            'POST',
            '/$/ReportClusterHealth',
            ['api-version=6.0', 'Immediate=true'],
            ('{"SourceId": "ID", '
             '"Property": "Property", '
             '"HealthState": "Warning", '
             '"TimeToLiveInMilliSeconds": "P3Y6M4DT12H30M5S", '
             '"Description": "Description", '
             '"SequenceNumber": "10", '
             '"RemoveWhenExpired": true}'),
            validate_flat_dictionary)
        self.validate_command(  # unprovision
            'sfctl cluster unprovision --code-version=code --config-version=config',
            'POST',
            '/$/Unprovision',
            ['api-version=6.0'],
            '{"CodeVersion":"code","ConfigVersion":"config"}',
            validate_flat_dictionary)
        self.validate_command(  # upgrade-resume
            'sfctl cluster upgrade-resume --upgrade-domain=UD2',
            'POST',
            '/$/MoveToNextUpgradeDomain',
            ['api-version=6.0'],
            '{"UpgradeDomain":"UD2"}',
            validate_flat_dictionary)
        self.validate_command(  # upgrade-rollback
            'sfctl cluster upgrade-rollback',
            'POST',
            '/$/RollbackUpgrade',
            ['api-version=6.0'])
        self.validate_command(  # upgrade-status
            'sfctl cluster upgrade-status',
            'GET',
            '/$/GetUpgradeProgress',
            ['api-version=6.0'])

        # Node Commands:
        self.validate_command(  # disable
            'sfctl node disable --node-name=nodeName --deactivation-intent=Pause',
            'POST',
            '/Nodes/nodeName/$/Deactivate',
            ['api-version=6.0'],
            '{"DeactivationIntent":"Pause"}',
            validate_flat_dictionary)
        self.validate_command(  # enable
            'sfctl node enable --node-name=nodeName',
            'POST',
            '/Nodes/nodeName/$/Activate',
            ['api-version=6.0'])
        self.validate_command(  # health
            'sfctl node health --node-name=nodeName --events-health-state-filter=2',
            'GET',
            '/Nodes/nodeName/$/GetHealth',
            ['api-version=6.0', 'EventsHealthStateFilter=2'])
        self.validate_command(  # info
            'sfctl node info --node-name=nodeName',
            'GET',
            '/Nodes/nodeName',
            ['api-version=6.0'])
        self.validate_command(  # list
            'sfctl node list --continuation-token=nodeId --node-status-filter=up',
            'GET',
            '/Nodes',
            ['api-version=6.0', 'ContinuationToken=nodeId', 'NodeStatusFilter=up'])
        self.validate_command(  # load
            'sfctl node load --node-name=nodeName',
            'GET',
            '/Nodes/nodeName/$/GetLoadInformation',
            ['api-version=6.0'])
        self.validate_command(  # remove-state
            'sfctl node remove-state --node-name=nodeName',
            'POST',
            '/Nodes/nodeName/$/RemoveNodeState',
            ['api-version=6.0'])
        self.validate_command(  # report-health
            'sfctl node report-health --node-name=nodeName --immediate --source-id=ID --health-property=Property ' +
            '--health-state=Warning --ttl=P3Y6M4DT12H30M5S --description=Description ' +
            '--sequence-number=10 --remove-when-expired=true',
            'POST',
            '/Nodes/nodeName/$/ReportHealth',
            ['api-version=6.0', 'Immediate=true'],
            ('{"SourceId": "ID", '
             '"Property": "Property", '
             '"HealthState": "Warning", '
             '"TimeToLiveInMilliSeconds": "P3Y6M4DT12H30M5S", '
             '"Description": "Description", '
             '"SequenceNumber": "10", '
             '"RemoveWhenExpired": true}'),
            validate_flat_dictionary)
        self.validate_command(  # restart
            'sfctl node restart --node-name=nodeName --node-instance-id=ID --create-fabric-dump=True',
            'POST',
            '/Nodes/nodeName/$/Restart',
            ['api-version=6.0'],
            '{"CreateFabricDump":"True", "NodeInstanceId":"ID"}',
            validate_flat_dictionary)

        # container commands
        self.validate_command(  # get container logs
            'sfctl container invoke-api --node-name Node01 --application-id samples/winnodejs '
            '--service-manifest-name NodeServicePackage --code-package-name NodeService.Code '
            '--code-package-instance-id 131668159770315380 --container-api-uri-path "/containers/{id}/logs?stdout=true&stderr=true"',
            'POST',
            '/Nodes/Node01/$/GetApplications/samples/winnodejs/$/GetCodePackages/$/ContainerApi',
            ['api-version=6.2', 'ServiceManifestName=NodeServicePackage', 'CodePackageName=NodeService.Code', 'CodePackageInstanceId=131668159770315380', 'timeout=60'],
            '{"UriPath": "/containers/{id}/logs?stdout=true&stderr=true"}',
            validate_flat_dictionary)
        self.validate_command(  # get container logs
            'sfctl container logs --node-name Node01 --application-id samples/winnodejs '
            '--service-manifest-name NodeServicePackage --code-package-name NodeService.Code '
            '--code-package-instance-id 131668159770315380',
            'POST',
            '/Nodes/Node01/$/GetApplications/samples/winnodejs/$/GetCodePackages/$/ContainerApi',
            ['api-version=6.2', 'ServiceManifestName=NodeServicePackage', 'CodePackageName=NodeService.Code', 'CodePackageInstanceId=131668159770315380', 'timeout=60'],
            '{"UriPath": "/containers/{id}/logs?stdout=true&stderr=true"}',
            validate_flat_dictionary)
        self.validate_command(  # update container
            'sfctl container invoke-api --node-name N0020 --application-id nodejs1 --service-manifest-name NodeOnSF '
            '--code-package-name Code --code-package-instance-id 131673596679688285 --container-api-uri-path "/containers/{id}/update"'
            ' --container-api-http-verb=POST --container-api-body "DummyRequestBody"',  # Manual testing with a JSON string for "--container-api-body" works,
            # Have to pass "DummyRequestBody" here since a real JSON string confuses test validation code.
            'POST',
            '/Nodes/N0020/$/GetApplications/nodejs1/$/GetCodePackages/$/ContainerApi',
            ['api-version=6.2', 'ServiceManifestName=NodeOnSF', 'CodePackageName=Code', 'CodePackageInstanceId=131673596679688285', 'timeout=60'],
            ('{"UriPath": "/containers/{id}/update", '
             '"HttpVerb": "POST", '
             '"Body": "DummyRequestBody"}'),
            validate_flat_dictionary)

        # Application Commands:
        # Application create tests not yet added
        # Application upgrade is not tested for all parameters
        # application upload tested as part of a custom command
        self.validate_command(  # delete
            'application delete --application-id=application~Id --force-remove=true',
            'POST',
            '/Applications/application~Id/$/Delete',
            ['api-version=6.0', 'ForceRemove=true'])
        self.validate_command(  # deployed
            'application deployed --application-id=application~Id --node-name=nodeName --include-health-state',
            'GET',
            '/Nodes/nodeName/$/GetApplications/application~Id',
            ['api-version=6.1', 'IncludeHealthState=true'])
        self.validate_command(  # deployed-list
            'application deployed-list --node-name=nodeName --continuation-token=token --include-health-state --max-results=10',
            'GET',
            '/Nodes/nodeName/$/GetApplications',
            ['api-version=6.1', 'ContinuationToken=token', 'IncludeHealthState=true', 'MaxResults=10'])
        self.validate_command(  # deployed-health
            'application deployed-health --node-name=nodeName --application-id=app~id --deployed-service-packages-health-state-filter=2 ' +
            '--events-health-state-filter=2 --exclude-health-statistics',
            'GET',
            '/Nodes/nodeName/$/GetApplications/app~id/$/GetHealth',
            ['api-version=6.0', 'EventsHealthStateFilter=2', 'ExcludeHealthStatistics=true', 'DeployedServicePackagesHealthStateFilter=2'])
        self.validate_command(  # health
            'application health --application-id=app~id --deployed-applications-health-state-filter=2 --services-health-state-filter=2 ' +
            '--events-health-state-filter=2 --exclude-health-statistics',
            'GET',
            '/Applications/app~id/$/GetHealth',
            ['api-version=6.0', 'EventsHealthStateFilter=2', 'ExcludeHealthStatistics=true', 'DeployedApplicationsHealthStateFilter=2',
             'ServicesHealthStateFilter=2'])
        self.validate_command(  # info
            'application info --application-id=application~Id --exclude-application-parameters',
            'GET',
            '/Applications/application~Id',
            ['api-version=6.0', 'ExcludeApplicationParameters=true'])
        self.validate_command(  # list
            'application list --application-type-name=name --continuation-token=token --exclude-application-parameters --max-results=10',
            'GET',
            '/Applications',
            ['api-version=6.1', 'ContinuationToken=token', 'ExcludeApplicationParameters=true', 'MaxResults=10', 'ApplicationTypeName=name'])
        self.validate_command(  # load
            'application load --application-id=application~Id',
            'GET',
            '/Applications/application~Id/$/GetLoadInformation',
            ['api-version=6.0'])
        self.validate_command(  # report-health
            'application report-health --application-id=id --immediate --source-id=ID --health-property=Property ' +
            '--health-state=Warning --ttl=P3Y6M4DT12H30M5S --description=Description ' +
            '--sequence-number=10 --remove-when-expired=true',
            'POST',
            '/Applications/id/$/ReportHealth',
            ['api-version=6.0', 'Immediate=true'],
            ('{"SourceId": "ID", '
             '"Property": "Property", '
             '"HealthState": "Warning", '
             '"TimeToLiveInMilliSeconds": "P3Y6M4DT12H30M5S", '
             '"Description": "Description", '
             '"SequenceNumber": "10", '
             '"RemoveWhenExpired": true}'),
            validate_flat_dictionary)

        app_params = path.join(sample_path_base, 'sample_application_parameters.txt').replace('/', '//').replace('\\', '\\\\')
        default_service_type_health_policy = path.join(sample_path_base, 'sample_default_service_type_health_policy.txt').replace('/', '//').replace('\\', '\\\\')  # pylint: disable=invalid-name
        service_type_health_policy_map = path.join(sample_path_base, 'sample_service_type_health_policy_map.txt').replace('/', '//').replace('\\', '\\\\')
        sample_application_capacity_metric_descriptions = path.join(sample_path_base, 'sample_application_capacity_metric_descriptions.txt').replace('/', '//').replace('\\', '\\\\')  # pylint: disable=invalid-name
        sample_application_parameters = path.join(sample_path_base, 'sample_application_parameters.txt').replace('/', '//').replace('\\', '\\\\')

        # application upgrade and application create does not currently test the body
        # Add this in later.
        self.validate_command(  # upgrade - not all parameters tested
            ('application upgrade '
             '--application-id=app '
             '--application-version=1.0.0 '
             '--parameters={0} '
             '--default-service-health-policy={1} '
             '--failure-action=Rollback '
             '--force-restart=true '
             '--health-check-retry-timeout=PT0H21M0S '
             '--health-check-stable-duration=PT0H21M0S '
             '--health-check-wait-duration=PT0H21M0S '
             '--max-unhealthy-apps=20 '
             '--mode=Monitored '
             '--replica-set-check-timeout=10 '
             '--service-health-policy={2} '
             '--upgrade-domain-timeout=some_timeout '
             '--upgrade-timeout=some_timeout2 '
             '--warning-as-error').format(
                 app_params, default_service_type_health_policy, service_type_health_policy_map),
            'POST',
            '/Applications/app/$/Upgrade',
            ['api-version=6.0'])

        self.validate_command(  # create
            ('application create '
             '--app-name=fabric:/app '
             '--app-type=test-type '
             '--app-version=1.0.0 '
             '--max-node-count=3 '
             '--min-node-count=1 '
             '--metrics={0} '
             '--parameters={1} ').format(sample_application_capacity_metric_descriptions, sample_application_parameters),
            'POST',
            '/Applications/$/Create',
            ['api-version=6.0'])

        self.validate_command(  # upgrade-resume
            'application upgrade-resume --application-id=application~Id --upgrade-domain-name=UD2',
            'POST',
            '/Applications/application~Id/$/MoveToNextUpgradeDomain',
            ['api-version=6.0'],
            '{"UpgradeDomainName":"UD2"}',
            validate_flat_dictionary)
        self.validate_command(  # upgrade-rollback
            'application upgrade-rollback --application-id=application~Id',
            'POST',
            '/Applications/application~Id/$/RollbackUpgrade',
            ['api-version=6.0'])
        self.validate_command(  # upgrade-status
            'application upgrade-status --application-id=application~Id',
            'GET',
            '/Applications/application~Id/$/GetUpgradeProgress',
            ['api-version=6.0'])

        # Compose
        # create is not tested here because it requires reading in a file.
        self.validate_command(  # list
            'compose list --continuation-token=token --max-results=10',
            'GET',
            '/ComposeDeployments',
            ['api-version=6.0-preview', 'ContinuationToken=token', 'MaxResults=10'])
        self.validate_command(  # status
            'compose status --deployment-name=deploymentName',
            'GET',
            '/ComposeDeployments/deploymentName',
            ['api-version=6.0-preview'])
        self.validate_command(  # remove
            'compose remove --deployment-name=deploymentName',
            'POST',
            '/ComposeDeployments/deploymentName/$/Delete',
            ['api-version=6.0-preview'])
        self.validate_command(  # upgrade-status
            'compose upgrade-status --deployment-name=deploymentName',
            'GET',
            '/ComposeDeployments/deploymentName/$/GetUpgradeProgress',
            ['api-version=6.0-preview'])

        # IS:
        self.validate_command(  # command
            'is command --command=cmd --service-id=id',
            'POST',
            '/$/InvokeInfrastructureCommand',
            ['api-version=6.0', 'Command=cmd', 'ServiceId=id'])
        self.validate_command(  # query
            'is query --command=cmd --service-id=id',
            'GET',
            '/$/InvokeInfrastructureQuery',
            ['api-version=6.0', 'Command=cmd', 'ServiceId=id'])

        # Partition
        self.validate_command(  # health
            'partition health --partition-id=id --events-health-state-filter=2 --exclude-health-statistics --replicas-health-state-filter=2',
            'GET',
            '/Partitions/id/$/GetHealth',
            ['api-version=6.0', 'EventsHealthStateFilter=2', 'ReplicasHealthStateFilter=2', 'ExcludeHealthStatistics=true'])
        self.validate_command(  # info
            'partition info --partition-id=id',
            'GET',
            '/Partitions/id',
            ['api-version=6.0'])
        self.validate_command(  # list
            'partition list --service-id=fabric:/app/id --continuation-token=ct',
            'GET',
            '/Services/fabric:/app/id/$/GetPartitions',
            ['api-version=6.0', 'ContinuationToken=ct'])
        self.validate_command(  # load
            'partition load --partition-id=id',
            'GET',
            '/Partitions/id/$/GetLoadInformation',
            ['api-version=6.0'])
        self.validate_command(  # load-reset
            'partition load-reset --partition-id=id',
            'POST',
            '/Partitions/id/$/ResetLoad',
            ['api-version=6.0'])
        self.validate_command(  # recover
            'partition recover --partition-id=id',
            'POST',
            '/Partitions/id/$/Recover',
            ['api-version=6.0'])
        self.validate_command(  # recover-all
            'partition recover-all',
            'POST',
            '/$/RecoverAllPartitions',
            ['api-version=6.0'])
        self.validate_command(  # svc-name
            'partition svc-name --partition-id=id',
            'GET',
            '/Partitions/id/$/GetServiceName',
            ['api-version=6.0'])
        self.validate_command(  # report-health
            'partition report-health --partition-id=id --immediate --source-id=ID --health-property=Property ' +
            '--health-state=Warning --ttl=P3Y6M4DT12H30M5S --description=Description ' +
            '--sequence-number=10 --remove-when-expired=true',
            'POST',
            '/Partitions/id/$/ReportHealth',
            ['api-version=6.0', 'Immediate=true'],
            ('{"SourceId": "ID", '
             '"Property": "Property", '
             '"HealthState": "Warning", '
             '"TimeToLiveInMilliSeconds": "P3Y6M4DT12H30M5S", '
             '"Description": "Description", '
             '"SequenceNumber": "10", '
             '"RemoveWhenExpired": true}'),
            validate_flat_dictionary)

        # Property
        value = '"{\\"Kind\\": \\"String\\", \\"Data\\": \\"data\\"}"'
        self.validate_command(  # put
            'property put --name-id=name --property-name=property --custom-id-type=type --value=' + value,
            'PUT',
            '/Names/name/$/GetProperty',
            ['api-version=6.0'],
            '{"PropertyName":"property", "CustomTypeId":"type", "Value":{"Kind": "String", "Data": "data"}}',
            validate_flat_dictionary)
        self.validate_command(  # get
            'property get --name-id=name --property-name=property',
            'GET',
            '/Names/name/$/GetProperty',
            ['api-version=6.0', 'PropertyName=property'])
        self.validate_command(  # list
            'property list --name-id=name --continuation-token=ct --include-values',
            'GET',
            '/Names/name/$/GetProperties',
            ['api-version=6.0', 'IncludeValues=true', 'ContinuationToken=ct'])
        self.validate_command(  # delete
            'property delete --name-id=name --property-name=property',
            'DELETE',
            '/Names/name/$/GetProperty',
            ['api-version=6.0', 'PropertyName=property'])

        # Replica
        self.validate_command(  # deployed
            'replica deployed --node-name=nodeName --partition-id=id --replica-id=replicaId',
            'GET',
            '/Nodes/nodeName/$/GetPartitions/id/$/GetReplicas/replicaId/$/GetDetail',
            ['api-version=6.0'])
        self.validate_command(  # deployed-list
            'replica deployed-list --node-name=nodeName --partition-id=id --application-id=applicationId --service-manifest-name=serviceManifestName',
            'GET',
            '/Nodes/nodeName/$/GetApplications/applicationId/$/GetReplicas',
            ['api-version=6.0', 'PartitionId=id', 'ServiceManifestName=serviceManifestName'])
        self.validate_command(  # health
            'replica health --events-health-state-filter=2 --partition-id=id --replica-id=replicaId',
            'GET',
            '/Partitions/id/$/GetReplicas/replicaId/$/GetHealth',
            ['api-version=6.0', 'EventsHealthStateFilter=2'])
        self.validate_command(  # info
            'replica info --partition-id=id --replica-id=replicaId',
            'GET',
            '/Partitions/id/$/GetReplicas/replicaId',
            ['api-version=6.0'])
        self.validate_command(  # list
            'replica list --continuation-token=ct --partition-id=id',
            'GET',
            '/Partitions/id/$/GetReplicas',
            ['api-version=6.0', 'ContinuationToken=ct'])
        self.validate_command(  # remove
            'replica remove --node-name=nodeName --partition-id=id --replica-id=replicaId --force-remove=true',
            'POST',
            '/Nodes/nodeName/$/GetPartitions/id/$/GetReplicas/replicaId/$/Delete',
            ['api-version=6.0', 'ForceRemove=true'])
        self.validate_command(  # report-health
            'replica report-health --partition-id=id --replica-id=replicaId --service-kind=Stateless --immediate --source-id=ID --health-property=Property ' +
            '--health-state=Warning --ttl=P3Y6M4DT12H30M5S --description=Description ' +
            '--sequence-number=10 --remove-when-expired=true',
            'POST',
            '/Partitions/id/$/GetReplicas/replicaId/$/ReportHealth',
            ['api-version=6.0', 'Immediate=true', 'ServiceKind=Stateless'],
            ('{"SourceId": "ID", '
             '"Property": "Property", '
             '"HealthState": "Warning", '
             '"TimeToLiveInMilliSeconds": "P3Y6M4DT12H30M5S", '
             '"Description": "Description", '
             '"SequenceNumber": "10", '
             '"RemoveWhenExpired": true}'),
            validate_flat_dictionary)
        self.validate_command(  # restart
            'replica restart --node-name=nodeName --partition-id=id --replica-id=replicaId',
            'POST',
            '/Nodes/nodeName/$/GetPartitions/id/$/GetReplicas/replicaId/$/Restart',
            ['api-version=6.0'])

        # RPM
        self.validate_command(  # approve-force
            'rpm approve-force --task-id=id --version=version',
            'POST',
            '/$/ForceApproveRepairTask',
            ['api-version=6.0'],
            '{"TaskId":"id", "Version":"version"}',
            validate_flat_dictionary)
        self.validate_command(  # delete
            'rpm delete --task-id=id --version=version',
            'POST',
            '/$/DeleteRepairTask',
            ['api-version=6.0'],
            '{"TaskId":"id", "Version":"version"}',
            validate_flat_dictionary)
        self.validate_command(  # list
            'rpm list --executor-filter=ex --state-filter=2 --task-id-filter=task',
            'GET',
            '/$/GetRepairTaskList',
            ['api-version=6.0', 'TaskIdFilter=task', 'StateFilter=2', 'ExecutorFilter=ex'])

        # Store
        self.validate_command(  # delete
            'store delete --content-path=path',
            'DELETE',
            '/ImageStore/path',
            ['api-version=6.0'])
        self.validate_command(  # root-info
            'store root-info',
            'GET',
            '/ImageStore',
            ['api-version=6.0'])
        self.validate_command(  # stat
            'store stat --content-path=path',
            'GET',
            '/ImageStore/path',
            ['api-version=6.2'])

        # Service
        # create and update tests not added for now
        self.validate_command(  # app-name
            'service app-name --service-id=some~service~path',
            'GET',
            '/Services/some~service~path/$/GetApplicationName',
            ['api-version=6.0'])
        self.validate_command(  # delete
            'service delete --service-id=some~service~path --force-remove=true',
            'POST',
            '/Services/some~service~path/$/Delete',
            ['api-version=6.0', 'ForceRemove=true'])
        self.validate_command(  # description
            'service description --service-id=some~service~path',
            'GET',
            '/Services/some~service~path/$/GetDescription',
            ['api-version=6.0'])
        self.validate_command(  # health
            'service health --service-id=some~service~path --events-health-state-filter=2 --exclude-health-statistics --partitions-health-state-filter=2',
            'GET',
            '/Services/some~service~path/$/GetHealth',
            ['api-version=6.0', 'EventsHealthStateFilter=2', 'PartitionsHealthStateFilter=2', 'ExcludeHealthStatistics=true'])
        self.validate_command(  # info
            'service info --service-id=some~service~path --application-id=app~id',
            'GET',
            '/Applications/app~id/$/GetServices/some~service~path',
            ['api-version=6.0'])
        self.validate_command(  # list
            'service list --service-type-name=type --application-id=app~id --continuation-token=ct',
            'GET',
            '/Applications/app~id/$/GetServices',
            ['api-version=6.0', 'ServiceTypeName=type', 'ContinuationToken=ct'])
        self.validate_command(  # resolve
            'service resolve --service-id=some~service~path --partition-key-type=3 --partition-key-value=part --previous-rsp-version=version',
            'GET',
            '/Services/some~service~path/$/ResolvePartition',
            ['api-version=6.0', 'PartitionKeyType=3', 'PartitionKeyValue=part', 'PreviousRspVersion=version'])
        self.validate_command(  # report-health
            'service report-health --service-id=service~id --immediate --source-id=ID --health-property=Property ' +
            '--health-state=Warning --ttl=P3Y6M4DT12H30M5S --description=Description ' +
            '--sequence-number=10 --remove-when-expired=true',
            'POST',
            '/Services/service~id/$/ReportHealth',
            ['api-version=6.0', 'Immediate=true'],
            ('{"SourceId": "ID", '
             '"Property": "Property", '
             '"HealthState": "Warning", '
             '"TimeToLiveInMilliSeconds": "P3Y6M4DT12H30M5S", '
             '"Description": "Description", '
             '"SequenceNumber": "10", '
             '"RemoveWhenExpired": true}'),
            validate_flat_dictionary)

        # Chaos commands:
        self.validate_command(  # get chaos schedule
            'chaos schedule set ' +
            '--version 0 --start-date-utc 2016-01-01T00:00:00.000Z ' +
            '--expiry-date-utc 2038-01-01T00:00:00.000Z ' +
            '--chaos-parameters-dictionary [{' +
            '\\\"Key\\\":\\\"adhoc\\\",\\\"Value\\\":{' +
            '\\\"MaxConcurrentFaults\\\":3,\\\"EnableMoveReplicaFaults\\\":true,' +
            '\\\"ChaosTargetFilter\\\":{\\\"NodeTypeInclusionList\\\":[' +
            '\\\"N0010Ref\\\",\\\"N0020Ref\\\",\\\"N0030Ref\\\",\\\"N0040Ref\\\",' +
            '\\\"N0050Ref\\\"]},\\\"MaxClusterStabilizationTimeoutInSeconds\\\":60,' +
            '\\\"WaitTimeBetweenIterationsInSeconds\\\":15,\\\"WaitTimeBetweenFaultsInSeconds\\\":30,' +
            '\\\"TimeToRunInSeconds\\\":\\\"600\\\",\\\"Context\\\":{\\\"Map\\\":{' +
            '\\\"test\\\":\\\"value\\\"}},\\\"ClusterHealthPolicy\\\":{' +
            '\\\"MaxPercentUnhealthyNodes\\\":0,\\\"ConsiderWarningAsError\\\":true,' +
            '\\\"MaxPercentUnhealthyApplications\\\":0}}}] ' +
            '--jobs [{\\\"ChaosParameters\\\":\\\"adhoc\\\",\\\"Days\\\":{' +
            '\\\"Sunday\\\":true,\\\"Monday\\\":true,\\\"Tuesday\\\":true,' +
            '\\\"Wednesday\\\":true,\\\"Thursday\\\":true,\\\"Friday\\\":true,' +
            '\\\"Saturday\\\":true},\\\"Times\\\":[{\\\"StartTime\\\":{' +
            '\\\"Hour\\\":0,\\\"Minute\\\":0},\\\"EndTime\\\":{' +
            '\\\"Hour\\\":23,\\\"Minute\\\":59}}]}]',
            'POST',
            '/Tools/Chaos/Schedule',
            ['api-version=6.2'])

        self.validate_command(  # get chaos schedule
            'chaos schedule get',
            'GET',
            '/Tools/Chaos/Schedule',
            ['api-version=6.2'])

        self.validate_command(  # stop chaos
            'chaos stop',
            'POST',
            '/Tools/Chaos/$/Stop',
            ['api-version=6.0'])

        self.validate_command(  # get chaos events
            'chaos events',
            'GET',
            '/Tools/Chaos/Events',
            ['api-version=6.2'])

        self.validate_command(  # get chaos
            'chaos get',
            'GET',
            '/Tools/Chaos',
            ['api-version=6.2'])
