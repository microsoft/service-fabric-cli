# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Custom chaos schedule command related tests"""
import unittest
import sfctl.custom_chaos_schedule as sf_c

#pylint: disable=invalid-name,line-too-long

class ChaosScheduleTests(unittest.TestCase):
    """Chaos Schedule tests"""

    def test_parse_none_time_of_day(self):
        """Parsing None TimeOfDay should return None"""

        res = sf_c.parse_time_of_day(None)
        self.assertIs(res, None)

    def test_parse_valid_time_of_day(self):
        """Parse a valid TimeOfDay"""

        res = sf_c.parse_time_of_day({
            'Hour': 23,
            'Minute': 59
        })


        self.assertEqual(res['Hour'], 23)
        self.assertEqual(res['Minute'], 59)

        res2 = sf_c.parse_time_of_day({
            'Hour': 0,
            'Minute': 0
        })

        self.assertEqual(res2['Hour'], 0)
        self.assertEqual(res2['Minute'], 0)

    def test_parse_none_time_range(self):
        """Parsing None TimeRange should return None"""

        res = sf_c.parse_time_range(None)
        self.assertIs(res, None)

    def test_parse_valid_time_range(self):
        """Parse a valid time range"""
        res = sf_c.parse_time_range({
            'StartTime': {
                'Hour': 0,
                'Minute': 0
            },
            'EndTime': {
                'Hour': 23,
                'Minute': 59,
            }
        })

        self.assertEqual(res['StartTime']['Hour'], 0)
        self.assertEqual(res['StartTime']['Minute'], 0)

        self.assertEqual(res['EndTime']['Hour'], 23)
        self.assertEqual(res['EndTime']['Minute'], 59)

    def test_parse_none_active_time_ranges(self):
        """Parsing None ActiveTimeRanges should return an empty list"""

        res = sf_c.parse_active_time_ranges(None)

        self.assertIsInstance(res, list)
        self.assertEqual(len(res), 0)

    def test_parse_valid_active_time_ranges(self):
        """Parse a list of valid time ranges"""

        res = sf_c.parse_active_time_ranges(
            [
                {
                    'StartTime': {
                        'Hour': 0,
                        'Minute': 0
                    },
                    'EndTime': {
                        'Hour': 12,
                        'Minute': 0,
                    }
                },
                {
                    'StartTime': {
                        'Hour': 12,
                        'Minute': 0
                    },
                    'EndTime': {
                        'Hour': 23,
                        'Minute': 59,
                    }
                }
            ]
        )

        self.assertIsInstance(res, list)
        self.assertEqual(len(res), 2)

        self.assertEqual(res[0]['StartTime']['Hour'], 0)
        self.assertEqual(res[0]['StartTime']['Minute'], 0)

        self.assertEqual(res[0]['EndTime']['Hour'], 12)
        self.assertEqual(res[0]['EndTime']['Minute'], 0)

        self.assertEqual(res[1]['StartTime']['Hour'], 12)
        self.assertEqual(res[1]['StartTime']['Minute'], 0)

        self.assertEqual(res[1]['EndTime']['Hour'], 23)
        self.assertEqual(res[1]['EndTime']['Minute'], 59)

    def test_parse_none_active_days(self):
        """Parsing None ChaosScheduleActiveDays should return None"""

        res = sf_c.parse_active_days(None)
        self.assertIs(res, None)

    def test_parse_valid_active_days(self):
        """Parse a valid active days"""

        res = sf_c.parse_active_days({
            'Monday': True,
            'Tuesday': True,
            'Wednesday': True,
            'Thursday': True,
            'Friday': True
        })

        self.assertEqual(res['Sunday'], False)
        self.assertEqual(res['Monday'], True)
        self.assertEqual(res['Tuesday'], True)
        self.assertEqual(res['Wednesday'], True)
        self.assertEqual(res['Thursday'], True)
        self.assertEqual(res['Friday'], True)
        self.assertEqual(res['Saturday'], False)

    def test_parse_none_job(self):
        """Parsing None ChaosScheduleJob should return None"""

        res = sf_c.parse_job(None)
        self.assertIs(res, None)

    def test_parse_valid_job(self):
        """Parse a valid ChaosScheduleJob"""

        res = sf_c.parse_job({
            'ChaosParameters': 'myParametersName',
            'Days': {
                'Monday': True,
                'Tuesday': True,
                'Wednesday': True,
                'Thursday': True,
                'Friday': True
            },
            'Times': [
                {
                    'StartTime': {
                        'Hour': 0,
                        'Minute': 0
                    },
                    'EndTime': {
                        'Hour': 6,
                        'Minute': 0,
                    }
                },
                {
                    'StartTime': {
                        'Hour': 18,
                        'Minute': 0
                    },
                    'EndTime': {
                        'Hour': 23,
                        'Minute': 59,
                    }
                }
            ]
        })


        self.assertEqual(res['ChaosParameters'], 'myParametersName')

        self.assertEqual(res['Days']['Sunday'], False)
        self.assertEqual(res['Days']['Monday'], True)
        self.assertEqual(res['Days']['Tuesday'], True)
        self.assertEqual(res['Days']['Wednesday'], True)
        self.assertEqual(res['Days']['Thursday'], True)
        self.assertEqual(res['Days']['Friday'], True)
        self.assertEqual(res['Days']['Saturday'], False)

        self.assertIsInstance(res['Times'], list)
        self.assertEqual(len(res['Times']), 2)

        self.assertEqual(res['Times'][0]['StartTime']['Hour'], 0)
        self.assertEqual(res['Times'][0]['StartTime']['Minute'], 0)

        self.assertEqual(res['Times'][0]['EndTime']['Hour'], 6)
        self.assertEqual(res['Times'][0]['EndTime']['Minute'], 0)


        self.assertEqual(res['Times'][1]['StartTime']['Hour'], 18)
        self.assertEqual(res['Times'][1]['StartTime']['Minute'], 0)

        self.assertEqual(res['Times'][1]['EndTime']['Hour'], 23)
        self.assertEqual(res['Times'][1]['EndTime']['Minute'], 59)

    def test_parse_none_jobs(self):
        """Parsing None ChaosScheduleJobs should return an empty list"""

        res = sf_c.parse_jobs(None)
        self.assertIsInstance(res, list)
        self.assertEqual(len(res), 0)

    def test_parse_valid_jobs(self):
        #pylint: disable=too-many-statements
        """Parse a valid list of ChaosScheduleJobs"""


        res = sf_c.parse_jobs([
            {
                'ChaosParameters': 'myParametersName',
                'Days': {
                    'Monday': True,
                    'Tuesday': True,
                    'Wednesday': True,
                    'Thursday': True,
                    'Friday': True
                },
                'Times': [
                    {
                        'StartTime': {
                            'Hour': 0,
                            'Minute': 0
                        },
                        'EndTime': {
                            'Hour': 6,
                            'Minute': 0,
                        }
                    },
                    {
                        'StartTime': {
                            'Hour': 18,
                            'Minute': 0
                        },
                        'EndTime': {
                            'Hour': 23,
                            'Minute': 59,
                        }
                    }
                ]
            },
            {
                'ChaosParameters': 'myOtherParametersName',
                'Days': {
                    'Sunday': True,
                    'Saturday': True,
                },
                'Times': [
                    {
                        'StartTime': {
                            'Hour': 12,
                            'Minute': 0
                        },
                        'EndTime': {
                            'Hour': 14,
                            'Minute': 0,
                        }
                    }
                ]
            }
        ])

        self.assertIsInstance(res, list)


        self.assertEqual(res[0]['ChaosParameters'], 'myParametersName')

        self.assertEqual(res[0]['Days']['Sunday'], False)
        self.assertEqual(res[0]['Days']['Monday'], True)
        self.assertEqual(res[0]['Days']['Tuesday'], True)
        self.assertEqual(res[0]['Days']['Wednesday'], True)
        self.assertEqual(res[0]['Days']['Thursday'], True)
        self.assertEqual(res[0]['Days']['Friday'], True)
        self.assertEqual(res[0]['Days']['Saturday'], False)

        self.assertIsInstance(res[0]['Times'], list)
        self.assertEqual(len(res[0]['Times']), 2)

        self.assertEqual(res[0]['Times'][0]['StartTime']['Hour'], 0)
        self.assertEqual(res[0]['Times'][0]['StartTime']['Minute'], 0)

        self.assertEqual(res[0]['Times'][0]['EndTime']['Hour'], 6)
        self.assertEqual(res[0]['Times'][0]['EndTime']['Minute'], 0)


        self.assertEqual(res[0]['Times'][1]['StartTime']['Hour'], 18)
        self.assertEqual(res[0]['Times'][1]['StartTime']['Minute'], 0)

        self.assertEqual(res[0]['Times'][1]['EndTime']['Hour'], 23)
        self.assertEqual(res[0]['Times'][1]['EndTime']['Minute'], 59)


        self.assertEqual(res[1]['ChaosParameters'], 'myOtherParametersName')
        self.assertEqual(res[1]['Days']['Sunday'], True)
        self.assertEqual(res[1]['Days']['Monday'], False)
        self.assertEqual(res[1]['Days']['Tuesday'], False)
        self.assertEqual(res[1]['Days']['Wednesday'], False)
        self.assertEqual(res[1]['Days']['Thursday'], False)
        self.assertEqual(res[1]['Days']['Friday'], False)
        self.assertEqual(res[1]['Days']['Saturday'], True)

        self.assertIsInstance(res[1]['Times'], list)
        self.assertEqual(len(res[1]['Times']), 1)

        self.assertEqual(res[1]['Times'][0]['StartTime']['Hour'], 12)
        self.assertEqual(res[1]['Times'][0]['StartTime']['Minute'], 0)

        self.assertEqual(res[1]['Times'][0]['EndTime']['Hour'], 14)
        self.assertEqual(res[1]['Times'][0]['EndTime']['Minute'], 0)
    def test_parse_none_chaos_parameters_dictionary(self):
        """Parsing None parameters dictionary should return an empty list"""

        res = sf_c.parse_chaos_params_dictionary(None)

        self.assertIsInstance(res, list)
        self.assertEqual(len(res), 0)

    def test_parse_valid_chaos_parameters_dictionary(self):
        #pylint: disable=too-many-statements
        """Parse a valid ChaosParametersDictionary"""


        res = sf_c.parse_chaos_params_dictionary([
            {
                'Key': 'myParametersName',
                'Value':  {
                    'MaxConcurrentFaults': 1,
                    'TimeToRunInSeconds': '600',
                    'MaxClusterStabilizationTimeoutInSeconds': 60,
                    'WaitTimeBetweenIterationsInSeconds': 15,
                    'WaitTimeBetweenFaultsInSeconds': 30,
                    'EnableMoveReplicaFaults': True,
                    'ClusterHealthPolicy': {
                        'MaxPercentUnhealthyNodes': 0,
                        'ConsiderWarningAsError': True,
                        'MaxPercentUnhealthyApplications': 0
                    },
                    'Context': {
                        'Map': {
                            'myContextKey': 'myContextValue'
                        }
                    },
                    'ChaosTargetFilter': {
                        'NodeTypeInclusionList': [
                            'N0010Ref',
                            'N0020Ref'
                        ]
                    }

                }
            },
            {
                'Key': 'myOtherParametersName',
                'Value': {
                    'MaxConcurrentFaults': 4,
                    'TimeToRunInSeconds': '300',
                    'MaxClusterStabilizationTimeoutInSeconds': 20,
                    'WaitTimeBetweenIterationsInSeconds': 10,
                    'WaitTimeBetweenFaultsInSeconds': 50,
                    'EnableMoveReplicaFaults': False,
                    'ClusterHealthPolicy': {
                        'MaxPercentUnhealthyNodes': 2,
                        'ConsiderWarningAsError': False,
                        'MaxPercentUnhealthyApplications': 5
                    },
                    'Context': {
                        'Map': {
                            'myOtherContextKey': 'myOtherContextValue'
                        }
                    },
                    'ChaosTargetFilter': {
                        'NodeTypeInclusionList': [
                            'N0030Ref',
                            'N0040Ref'
                        ]
                    }

                }
            }
        ])

        self.assertIsInstance(res, list)
        self.assertEqual(len(res), 2)

        self.assertEqual(res[0]['Key'], 'myParametersName')

        self.assertEqual(res[0]['Value']['TimeToRunInSeconds'], '600')
        self.assertEqual(
            res[0]['Value']['MaxClusterStabilizationTimeoutInSeconds'], 60)
        self.assertEqual(res[0]['Value']['MaxConcurrentFaults'], 1)
        self.assertEqual(res[0]['Value']['EnableMoveReplicaFaults'], True)
        self.assertEqual(res[0]['Value']['WaitTimeBetweenFaultsInSeconds'], 30)
        self.assertEqual(
            res[0]['Value']['WaitTimeBetweenIterationsInSeconds'], 15)

        cluster_health_policy = res[0]['Value']['ClusterHealthPolicy']

        self.assertEqual(cluster_health_policy['MaxPercentUnhealthyNodes'], 0)
        self.assertEqual(cluster_health_policy['ConsiderWarningAsError'], True)
        self.assertEqual(
            cluster_health_policy['MaxPercentUnhealthyApplications'], 0)

        self.assertIsInstance(res[0]['Value']['Context']['Map'], dict)
        self.assertEqual(
            res[0]['Value']['Context']['Map']['myContextKey'], 'myContextValue')

        chaos_target_filter = res[0]['Value']['ChaosTargetFilter']

        self.assertIsInstance(
            chaos_target_filter['NodeTypeInclusionList'], list)
        self.assertEqual(len(chaos_target_filter['NodeTypeInclusionList']), 2)
        self.assertEqual(
            chaos_target_filter['NodeTypeInclusionList'][0], 'N0010Ref')
        self.assertEqual(
            chaos_target_filter['NodeTypeInclusionList'][1], 'N0020Ref')

        self.assertEqual(res[1]['Key'], 'myOtherParametersName')

        self.assertEqual(res[1]['Value']['TimeToRunInSeconds'], '300')
        self.assertEqual(
            res[1]['Value']['MaxClusterStabilizationTimeoutInSeconds'], 20)
        self.assertEqual(res[1]['Value']['MaxConcurrentFaults'], 4)
        self.assertEqual(res[1]['Value']['EnableMoveReplicaFaults'], False)
        self.assertEqual(res[1]['Value']['WaitTimeBetweenFaultsInSeconds'], 50)
        self.assertEqual(
            res[1]['Value']['WaitTimeBetweenIterationsInSeconds'], 10)

        cluster_health_policy2 = res[1]['Value']['ClusterHealthPolicy']

        self.assertEqual(cluster_health_policy2['MaxPercentUnhealthyNodes'], 2)
        self.assertEqual(
            cluster_health_policy2['ConsiderWarningAsError'], False)
        self.assertEqual(
            cluster_health_policy2['MaxPercentUnhealthyApplications'], 5)

        self.assertIsInstance(res[1]['Value']['Context']['Map'], dict)
        self.assertEqual(res[1]['Value']['Context']['Map']['myOtherContextKey'],
            'myOtherContextValue')

        chaos_target_filter2 = res[1]['Value']['ChaosTargetFilter']

        self.assertIsInstance(
            chaos_target_filter2['NodeTypeInclusionList'], list)
        self.assertEqual(
            len(chaos_target_filter2['NodeTypeInclusionList']), 2)
        self.assertEqual(
            chaos_target_filter2['NodeTypeInclusionList'][0],
            'N0030Ref')
        self.assertEqual(
            chaos_target_filter2['NodeTypeInclusionList'][1],
            'N0040Ref')
