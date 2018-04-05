# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Custom Chaos command related tests"""

import unittest
import sfctl.custom_chaos as sf_c


class ChaosTests(unittest.TestCase):
    """Chaos tests"""

    def test_parse_none_context(self):
        """Parsing None context returns None"""
        res = sf_c.parse_chaos_context(None)
        self.assertIs(res, None)

    def test_parse_populated_context(self):
        """Parse context with contents"""
        from azure.servicefabric.models.chaos_context import (
            ChaosContext
        )

        wrapper = sf_c.parse_chaos_context({
            'key1': 'value1',
            'key2': 'value2',
            'key3': 'value3'
        })

        self.assertIsInstance(wrapper, ChaosContext)
        res = wrapper.map
        self.assertIsInstance(res, dict)
        self.assertEqual(len(res), 3)
        self.assertEqual(res['key1'], 'value1')
        self.assertEqual(res['key2'], 'value2')
        self.assertEqual(res['key3'], 'value3')

    def test_parse_none_target_filter(self):
        """Parse None chaos target filter returns None"""
        self.assertIs(sf_c.parse_chaos_target_filter(None), None)

    def test_parse_node_type_list(self):
        """Parse NodeTypeInclusionList list"""

        res = sf_c.parse_chaos_target_filter({
            'NodeTypeInclusionList': [
                'N0010Ref', 'N0020Ref', 'N0030Ref', 'N0070Ref']
        })

        self.assertEqual(len(res.node_type_inclusion_list), 4)
        self.assertEqual(res.application_inclusion_list, None)
        self.assertEqual(res.node_type_inclusion_list[0], 'N0010Ref')
        self.assertEqual(res.node_type_inclusion_list[1], 'N0020Ref')
        self.assertEqual(res.node_type_inclusion_list[2], 'N0030Ref')
        self.assertEqual(res.node_type_inclusion_list[3], 'N0070Ref')

    def test_parse_application_list(self):
        """Parse application inclusion list"""

        res = sf_c.parse_chaos_target_filter({
            'ApplicationInclusionList': ['fabric:/TestApp1', 'fabric:/TestApp2']  # pylint: disable=line-too-long
        })

        self.assertEqual(len(res.application_inclusion_list), 2)
        self.assertEqual(res.node_type_inclusion_list, None)
        self.assertEqual(res.application_inclusion_list[0], 'fabric:/TestApp1')
        self.assertEqual(res.application_inclusion_list[1], 'fabric:/TestApp2')
