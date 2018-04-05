# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Custom health command related tests"""
import unittest
import sfctl.custom_health as sf_c


# pylint: disable=invalid-name

class HealthTests(unittest.TestCase):
    """Health tests"""

    def test_parse_none_svc_health_policy(self):
        """Parsing None service health policy returns None"""
        res = sf_c.parse_service_health_policy(None)
        self.assertIs(res, None)

    def test_parse_single_svc_health_policy(self):
        """Parse single health policy item"""
        from azure.servicefabric.models.service_type_health_policy import (
            ServiceTypeHealthPolicy
        )

        res = sf_c.parse_service_health_policy({
            'max_percent_unhealthy_partitions_per_service': 10,
            'max_percent_unhealthy_replicas_per_partition': 20,
            'max_percent_unhealthy_services': 25
        })
        self.assertIsInstance(res, ServiceTypeHealthPolicy)
        self.assertEqual(res.max_percent_unhealthy_partitions_per_service, 10)
        self.assertEqual(res.max_percent_unhealthy_replicas_per_partition, 20)
        self.assertEqual(res.max_percent_unhealthy_services, 25)

    def test_parse_none_svc_health_policy_map(self):
        """Parse None service health policy map returns None"""
        self.assertIs(sf_c.parse_service_health_policy_map(None), None)

    def test_parse_empty_svc_health_policy_map(self):
        """Parse empty service health policy map returns empty list"""
        self.assertEqual(sf_c.parse_service_health_policy_map(''), [])

    def test_parse_single_svc_health_policy_map_item(self):
        """Parse single item service health policy map"""
        from azure.servicefabric.models.service_type_health_policy_map_item import ServiceTypeHealthPolicyMapItem  # pylint: disable=line-too-long

        res = sf_c.parse_service_health_policy_map([{
            'Key': 'test_svc',
            'Value': {
                'max_percent_unhealthy_partitions_per_service': 10,
                'max_percent_unhealthy_replicas_per_partition': 20,
                'max_percent_unhealthy_services': 25
            }
        }])

        self.assertEqual(len(res), 1)
        self.assertIsInstance(res[0], ServiceTypeHealthPolicyMapItem)
        res = res[0].value
        self.assertEqual(res.max_percent_unhealthy_partitions_per_service, 10)
        self.assertEqual(res.max_percent_unhealthy_replicas_per_partition, 20)
        self.assertEqual(res.max_percent_unhealthy_services, 25)

    def test_parse_none_app_health_map(self):
        """Parse None application health policy map returns None"""
        self.assertIs(sf_c.parse_app_health_map(None), None)

    def test_parse_empty_app_health_map(self):
        """Parse empty application health policy map returns None"""
        self.assertIs(sf_c.parse_app_health_map(''), None)

    def test_parse_single_app_health_map_item(self):
        """Parse single item application health policy map"""
        from azure.servicefabric.models.application_type_health_policy_map_item import ApplicationTypeHealthPolicyMapItem  # pylint: disable=line-too-long

        res = sf_c.parse_app_health_map([{'key': 'test_app', 'value': '30'}])
        self.assertEqual(len(res), 1)
        res = res[0]
        self.assertIsInstance(res, ApplicationTypeHealthPolicyMapItem)
        self.assertEqual(res.key, 'test_app')
        self.assertEqual(res.value, '30')
