# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Custom service command tests"""

import unittest
from knack.util import CLIError
import sfctl.custom_service as sf_c


# pylint: disable=invalid-name

class ServiceTests(unittest.TestCase):  # pylint: disable=too-many-public-methods
    """Service tests"""

    def test_parse_none_correlation_desc(self):
        """Parse None correlation description returns None"""
        self.assertIs(sf_c.correlation_desc(None, None), None)

    def test_parse_partial_correlation_desc(self):
        """Parse partial correlation description raises error"""
        with self.assertRaises(CLIError):
            sf_c.correlation_desc('test_svc', None)

    def test_parse_complete_correlation_desc(self):
        """Parse a single correlation description"""
        res = sf_c.correlation_desc('test', 'Affinity')
        self.assertEqual(res.service_name, 'test')
        self.assertEqual(res.scheme, 'Affinity')

    def test_parse_empty_load_metrics(self):
        """Parse empty load metrics returns None"""
        self.assertIsNone(sf_c.parse_load_metrics(''))

    def test_parse_none_load_metrics(self):
        """Parse none load metrics returns None"""
        self.assertIsNone(sf_c.parse_load_metrics(None))

    def test_parse_scaling_policy_test(self):
        """Parse scaling policies"""
        res = sf_c.parse_scaling_policy([{
            'mechanism':{'kind':'PartitionInstanceCount', 'min_instance_count':2, 'max_instance_count':4, 'scale_increment':2}, #pylint: disable=line-too-long
            'trigger':{'kind':'AveragePartitionLoad', 'metric_name':'MetricA', 'upper_load_threshold':20.0, 'lower_load_threshold':10.0, 'scale_interval_in_seconds':1000} #pylint: disable=line-too-long
        }, {
            'mechanism':{'kind':'AddRemoveIncrementalNamedPartition', 'min_partition_count':3, 'max_partition_count':6, 'scale_increment':2}, #pylint: disable=line-too-long
            'trigger':{'kind':'AverageServiceLoad', 'metric_name':'MetricB', 'upper_load_threshold':30.0, 'lower_load_threshold':10.0, 'scale_interval_in_seconds':1000} #pylint: disable=line-too-long
        }])
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0].scaling_trigger.metric_name, 'MetricA')
        self.assertEqual(res[0].scaling_trigger.upper_load_threshold, 20.0)
        self.assertEqual(res[0].scaling_trigger.lower_load_threshold, 10.0)
        self.assertEqual(res[0].scaling_mechanism.max_instance_count, 4)
        self.assertEqual(res[1].scaling_trigger.scale_interval_in_seconds, 1000)
        self.assertEqual(res[1].scaling_trigger.upper_load_threshold, 30.0)
        self.assertEqual(res[1].scaling_trigger.lower_load_threshold, 10.0)
        self.assertEqual(res[1].scaling_mechanism.scale_increment, 2)

    def test_parse_incomplete_load_metrics(self):
        """Parse single incomplete load metrics definition"""

        res = sf_c.parse_load_metrics([{'name': 'test_metric',
                                        'default_load': 10}])

        self.assertEqual(len(res), 1)
        res = res[0]
        self.assertEqual(res.name, 'test_metric')
        self.assertIsNone(res.weight)
        self.assertIsNone(res.primary_default_load)
        self.assertIsNone(res.secondary_default_load)
        self.assertEqual(res.default_load, 10)

    def test_parse_invalid_placement_policy_type(self):
        """Parsing invalid placement policy type raises error"""
        with self.assertRaises(CLIError):
            sf_c.parse_placement_policies([{'type': 'test',
                                            'domain_name': 'test'}])

    def test_parse_missing_placement_policy_domain_name(self):
        """Parsing missing domain name in placement policy raises error"""
        with self.assertRaises(CLIError):
            sf_c.parse_placement_policies([{'type': 'PreferPrimaryDomain'}])

    def test_parse_all_placement_policy_types(self):
        """Parse all placement policy types"""

        from azure.servicefabric.models.service_placement_non_partially_place_service_policy_description import ServicePlacementNonPartiallyPlaceServicePolicyDescription  # pylint: disable=line-too-long
        from azure.servicefabric.models.service_placement_prefer_primary_domain_policy_description import ServicePlacementPreferPrimaryDomainPolicyDescription  # pylint: disable=line-too-long
        from azure.servicefabric.models.service_placement_required_domain_policy_description import ServicePlacementRequiredDomainPolicyDescription  # pylint: disable=line-too-long
        from azure.servicefabric.models.service_placement_require_domain_distribution_policy_description import ServicePlacementRequireDomainDistributionPolicyDescription  # pylint: disable=line-too-long

        res = sf_c.parse_placement_policies([{
            'type': 'NonPartiallyPlaceService'
        }, {
            'type': 'PreferPrimaryDomain',
            'domain_name': 'test_1'
        }, {
            'type': 'RequireDomain',
            'domain_name': 'test-22'
        }, {
            'type': 'RequireDomainDistribution',
            'domain_name': 'test_3'
        }])
        self.assertIsInstance(
            res[0],
            ServicePlacementNonPartiallyPlaceServicePolicyDescription
        )
        self.assertIsInstance(
            res[1],
            ServicePlacementPreferPrimaryDomainPolicyDescription
        )
        self.assertEqual(res[1].domain_name, 'test_1')
        self.assertIsInstance(
            res[2],
            ServicePlacementRequiredDomainPolicyDescription
        )
        self.assertEqual(res[2].domain_name, 'test-22')
        self.assertIsInstance(
            res[3],
            ServicePlacementRequireDomainDistributionPolicyDescription
        )
        self.assertEqual(res[3].domain_name, 'test_3')

    def test_invalid_move_cost(self):
        """Invalid move cost raises error"""
        with self.assertRaises(CLIError):
            sf_c.validate_move_cost('test')

    def test_empty_stateful_flags(self):
        """Empty stateful flags returns zero"""
        self.assertEqual(sf_c.stateful_flags(), 0)

    def test_all_stateful_flags(self):
        """All stateful flags sum up to correct value"""
        self.assertEqual(sf_c.stateful_flags(10, 10, 10), 7)

    def test_empty_service_update_flags(self):
        """Empty service update flags returns zero"""
        self.assertEqual(sf_c.service_update_flags(), 0)

    def test_all_service_update_flags(self):
        """All service update flags sum up to correct value"""
        self.assertEqual(sf_c.service_update_flags(target_rep_size=1,
                                                   rep_restart_wait=10,
                                                   quorum_loss_wait=10,
                                                   standby_rep_keep=10,
                                                   min_rep_size=5,
                                                   placement_constraints='',
                                                   placement_policy='',
                                                   correlation='',
                                                   metrics='',
                                                   move_cost='high'), 1023)

    def test_service_create_missing_service_state(self):
        """Service create must specify exactly stateful or stateless"""
        with self.assertRaises(CLIError):
            sf_c.validate_service_create_params(False, False, None, None,
                                                None, None, None, None)
        with self.assertRaises(CLIError):
            sf_c.validate_service_create_params(True, True, None, None, None,
                                                None, None, None)

    def test_service_create_target_size_matches_state(self):
        """Service create target replica set and instance count match
        stateful or stateless"""
        with self.assertRaises(CLIError):
            sf_c.validate_service_create_params(True, False, True, False,
                                                False, 10, None, None)
        with self.assertRaises(CLIError):
            sf_c.validate_service_create_params(False, True, True, False,
                                                False, None, 10, None)

    def test_service_create_missing_stateful_replica_set_sizes(self):
        """Service create without target or min replica set sizes raises
        error"""
        with self.assertRaises(CLIError):
            sf_c.validate_service_create_params(True, False, True, False,
                                                False, None, 10, None)

    def test_parse_incomplete_partition_policy_named_scheme(self):
        """Parsing named partition policy with unspecified names raises
        error"""
        with self.assertRaises(CLIError):
            sf_c.parse_partition_policy(True, None, None, None, None, None,
                                        None)

    def test_parse_incomplete_partition_policy_int(self):
        """Parsing int partition policy with incomplete args raises error"""
        with self.assertRaises(CLIError):
            sf_c.parse_partition_policy(False, None, True, 0, 5, None, False)

    def test_parse_multiple_partition_policy(self):
        """Parsing multiple different partition polices raises error"""
        with self.assertRaises(CLIError):
            sf_c.parse_partition_policy(True, ['test'], True, 0, 5, 3, True)

    def test_parse_valid_partition_policy(self):
        """Parsing valid partition polices returns correct policies"""
        from azure.servicefabric.models.named_partition_scheme_description import NamedPartitionSchemeDescription  # pylint: disable=line-too-long
        from azure.servicefabric.models.singleton_partition_scheme_description import SingletonPartitionSchemeDescription  # pylint:disable=line-too-long
        from azure.servicefabric.models.uniform_int64_range_partition_scheme_description import UniformInt64RangePartitionSchemeDescription  # pylint:disable=line-too-long

        res = sf_c.parse_partition_policy(True, ['test'], False, None, None,
                                          None, False)
        self.assertIsInstance(res, NamedPartitionSchemeDescription)
        self.assertEqual(res.count, 1)
        self.assertEqual(res.names, ['test'])

        res = sf_c.parse_partition_policy(False, None, True, 1, 5, 3, False)
        self.assertIsInstance(res, UniformInt64RangePartitionSchemeDescription)
        self.assertEqual(res.high_key, 5)
        self.assertEqual(res.low_key, 1)
        self.assertEqual(res.count, 3)

        res = sf_c.parse_partition_policy(False, None, False, None, None, None,
                                          True)
        self.assertIsInstance(res, SingletonPartitionSchemeDescription)

    def test_activation_mode_invalid(self):
        """Invalid activation mode specified raises error"""
        with self.assertRaises(CLIError):
            sf_c.validate_activation_mode('test')

    def test_activation_mode_none(self):  # pylint: disable=no-self-use
        """None activation mode is considered valid"""
        sf_c.validate_activation_mode(None)

    def test_service_update_specify_state(self):
        """Service update incorrectly specifying service state raises error"""
        with self.assertRaises(CLIError):
            sf_c.validate_update_service_params(False, False, 10, 0, 10,
                                                10, 10, False)

    def test_service_update_stateful_invalid_params(self):
        """Stateful service update with invalid args raises error"""
        with self.assertRaises(CLIError):
            sf_c.validate_update_service_params(False, True, 5, 3, 10,
                                                10, 10, 1)

    def test_service_update_stateless_invalid_params(self):
        """Stateless service update with invalid args raises error"""
        with self.assertRaises(CLIError):
            sf_c.validate_update_service_params(True, False, 5, None, None,
                                                None, None, 10)
        with self.assertRaises(CLIError):
            sf_c.validate_update_service_params(True, False, None, 1, None,
                                                None, None, 10)
        with self.assertRaises(CLIError):
            sf_c.validate_update_service_params(True, False, None, None, 10,
                                                None, None, 10)
        with self.assertRaises(CLIError):
            sf_c.validate_update_service_params(True, False, None, None, None,
                                                10, None, 10)
        with self.assertRaises(CLIError):
            sf_c.validate_update_service_params(True, False, None, None, None,
                                                None, 5, 10)
