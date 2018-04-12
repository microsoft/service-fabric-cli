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
        from azure.servicefabric.models.time_of_day import (
            TimeOfDay
        )

        res = sf_c.parse_time_of_day({
            'Hour': 23,
            'Minute': 59
        })

        self.assertIsInstance(res, TimeOfDay)

        self.assertEqual(res.hour, 23)
        self.assertEqual(res.minute, 59)

        res2 = sf_c.parse_time_of_day({
            'Hour': 0,
            'Minute': 0
        })

        self.assertIsInstance(res2, TimeOfDay)

        self.assertEqual(res2.hour, 0)
        self.assertEqual(res2.minute, 0)

    def test_parse_none_time_range(self):
        """Parsing None TimeRange should return None"""

        res = sf_c.parse_time_range(None)
        self.assertIs(res, None)

    def test_parse_valid_time_range(self):
        """Parse a valid time range"""
        from azure.servicefabric.models.time_range import (
            TimeRange
        )
        from azure.servicefabric.models.time_of_day import (
            TimeOfDay
        )

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

        self.assertIsInstance(res, TimeRange)

        self.assertIsInstance(res.start_time, TimeOfDay)
        self.assertEqual(res.start_time.hour, 0)
        self.assertEqual(res.start_time.minute, 0)

        self.assertIsInstance(res.end_time, TimeOfDay)
        self.assertEqual(res.end_time.hour, 23)
        self.assertEqual(res.end_time.minute, 59)

    def test_parse_none_active_time_ranges(self):
        """Parsing None ActiveTimeRanges should return an empty list"""

        res = sf_c.parse_active_time_ranges(None)

        self.assertIsInstance(res, list)
        self.assertEqual(len(res), 0)

    def test_parse_valid_active_time_ranges(self):
        """Parse a list of valid time ranges"""
        from azure.servicefabric.models.time_range import (
            TimeRange
        )
        from azure.servicefabric.models.time_of_day import (
            TimeOfDay
        )

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

        self.assertIsInstance(res[0], TimeRange)
        self.assertIsInstance(res[0].start_time, TimeOfDay)
        self.assertEqual(res[0].start_time.hour, 0)
        self.assertEqual(res[0].start_time.minute, 0)

        self.assertIsInstance(res[0].end_time, TimeOfDay)
        self.assertEqual(res[0].end_time.hour, 12)
        self.assertEqual(res[0].end_time.minute, 0)

        self.assertIsInstance(res[1], TimeRange)
        self.assertIsInstance(res[1].start_time, TimeOfDay)
        self.assertEqual(res[1].start_time.hour, 12)
        self.assertEqual(res[1].start_time.minute, 0)

        self.assertIsInstance(res[1].end_time, TimeOfDay)
        self.assertEqual(res[1].end_time.hour, 23)
        self.assertEqual(res[1].end_time.minute, 59)

    def test_parse_none_active_days(self):
        """Parsing None ChaosScheduleActiveDays should return None"""

        res = sf_c.parse_active_days(None)
        self.assertIs(res, None)

    def test_parse_valid_active_days(self):
        """Parse a valid active days"""
        from azure.servicefabric.models.chaos_schedule_job_active_days_of_week import (
            ChaosScheduleJobActiveDaysOfWeek
        )

        res = sf_c.parse_active_days({
            'Monday': True,
            'Tuesday': True,
            'Wednesday': True,
            'Thursday': True,
            'Friday': True
        })

        self.assertIsInstance(res, ChaosScheduleJobActiveDaysOfWeek)
        self.assertEqual(res.sunday, False)
        self.assertEqual(res.monday, True)
        self.assertEqual(res.tuesday, True)
        self.assertEqual(res.wednesday, True)
        self.assertEqual(res.thursday, True)
        self.assertEqual(res.friday, True)
        self.assertEqual(res.saturday, False)

    def test_parse_none_job(self):
        """Parsing None ChaosScheduleJob should return None"""

        res = sf_c.parse_job(None)
        self.assertIs(res, None)

    def test_parse_valid_job(self):
        """Parse a valid ChaosScheduleJob"""
        from azure.servicefabric.models.time_range import (
            TimeRange
        )
        from azure.servicefabric.models.time_of_day import (
            TimeOfDay
        )
        from azure.servicefabric.models.chaos_schedule_job_active_days_of_week import (
            ChaosScheduleJobActiveDaysOfWeek
        )
        from azure.servicefabric.models.chaos_schedule_job import (
            ChaosScheduleJob
        )

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

        self.assertIsInstance(res, ChaosScheduleJob)

        self.assertEqual(res.chaos_parameters, 'myParametersName')

        self.assertIsInstance(res.days, ChaosScheduleJobActiveDaysOfWeek)
        self.assertEqual(res.days.sunday, False)
        self.assertEqual(res.days.monday, True)
        self.assertEqual(res.days.tuesday, True)
        self.assertEqual(res.days.wednesday, True)
        self.assertEqual(res.days.thursday, True)
        self.assertEqual(res.days.friday, True)
        self.assertEqual(res.days.saturday, False)

        self.assertIsInstance(res.times, list)
        self.assertEqual(len(res.times), 2)

        self.assertIsInstance(res.times[0], TimeRange)
        self.assertIsInstance(res.times[0].start_time, TimeOfDay)
        self.assertEqual(res.times[0].start_time.hour, 0)
        self.assertEqual(res.times[0].start_time.minute, 0)
        self.assertIsInstance(res.times[0].end_time, TimeOfDay)
        self.assertEqual(res.times[0].end_time.hour, 6)
        self.assertEqual(res.times[0].end_time.minute, 0)

        self.assertIsInstance(res.times[1], TimeRange)
        self.assertIsInstance(res.times[1].start_time, TimeOfDay)
        self.assertEqual(res.times[1].start_time.hour, 18)
        self.assertEqual(res.times[1].start_time.minute, 0)
        self.assertIsInstance(res.times[1].end_time, TimeOfDay)
        self.assertEqual(res.times[1].end_time.hour, 23)
        self.assertEqual(res.times[1].end_time.minute, 59)

    def test_parse_none_jobs(self):
        """Parsing None ChaosScheduleJobs should return an empty list"""

        res = sf_c.parse_jobs(None)
        self.assertIsInstance(res, list)
        self.assertEqual(len(res), 0)

    def test_parse_valid_jobs(self):
        #pylint: disable=too-many-statements
        """Parse a valid list of ChaosScheduleJobs"""
        from azure.servicefabric.models.time_range import (
            TimeRange
        )
        from azure.servicefabric.models.time_of_day import (
            TimeOfDay
        )
        from azure.servicefabric.models.chaos_schedule_job_active_days_of_week import (
            ChaosScheduleJobActiveDaysOfWeek
        )
        from azure.servicefabric.models.chaos_schedule_job import (
            ChaosScheduleJob
        )

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

        self.assertIsInstance(res[0], ChaosScheduleJob)
        self.assertEqual(res[0].chaos_parameters, 'myParametersName')

        self.assertIsInstance(res[0].days, ChaosScheduleJobActiveDaysOfWeek)
        self.assertEqual(res[0].days.sunday, False)
        self.assertEqual(res[0].days.monday, True)
        self.assertEqual(res[0].days.tuesday, True)
        self.assertEqual(res[0].days.wednesday, True)
        self.assertEqual(res[0].days.thursday, True)
        self.assertEqual(res[0].days.friday, True)
        self.assertEqual(res[0].days.saturday, False)

        self.assertIsInstance(res[0].times, list)
        self.assertEqual(len(res[0].times), 2)

        self.assertIsInstance(res[0].times[0], TimeRange)
        self.assertIsInstance(res[0].times[0].start_time, TimeOfDay)
        self.assertEqual(res[0].times[0].start_time.hour, 0)
        self.assertEqual(res[0].times[0].start_time.minute, 0)
        self.assertIsInstance(res[0].times[0].end_time, TimeOfDay)
        self.assertEqual(res[0].times[0].end_time.hour, 6)
        self.assertEqual(res[0].times[0].end_time.minute, 0)

        self.assertIsInstance(res[0].times[1], TimeRange)
        self.assertIsInstance(res[0].times[1].start_time, TimeOfDay)
        self.assertEqual(res[0].times[1].start_time.hour, 18)
        self.assertEqual(res[0].times[1].start_time.minute, 0)
        self.assertIsInstance(res[0].times[1].end_time, TimeOfDay)
        self.assertEqual(res[0].times[1].end_time.hour, 23)
        self.assertEqual(res[0].times[1].end_time.minute, 59)

        self.assertIsInstance(res[1], ChaosScheduleJob)
        self.assertEqual(res[1].chaos_parameters, 'myOtherParametersName')

        self.assertIsInstance(res[1].days, ChaosScheduleJobActiveDaysOfWeek)
        self.assertEqual(res[1].days.sunday, True)
        self.assertEqual(res[1].days.monday, False)
        self.assertEqual(res[1].days.tuesday, False)
        self.assertEqual(res[1].days.wednesday, False)
        self.assertEqual(res[1].days.thursday, False)
        self.assertEqual(res[1].days.friday, False)
        self.assertEqual(res[1].days.saturday, True)

        self.assertIsInstance(res[1].times, list)
        self.assertEqual(len(res[1].times), 1)

        self.assertIsInstance(res[1].times[0], TimeRange)
        self.assertIsInstance(res[1].times[0].start_time, TimeOfDay)
        self.assertEqual(res[1].times[0].start_time.hour, 12)
        self.assertEqual(res[1].times[0].start_time.minute, 0)
        self.assertIsInstance(res[1].times[0].end_time, TimeOfDay)
        self.assertEqual(res[1].times[0].end_time.hour, 14)
        self.assertEqual(res[1].times[0].end_time.minute, 0)

    def test_parse_none_chaos_parameters_dictionary(self):
        """Parsing None parameters dictionary should return an empty list"""

        res = sf_c.parse_chaos_params_dictionary(None)

        self.assertIsInstance(res, list)
        self.assertEqual(len(res), 0)

    def test_parse_valid_chaos_parameters_dictionary(self):
        #pylint: disable=too-many-statements
        """Parse a valid ChaosParametersDictionary"""
        from azure.servicefabric.models.chaos_parameters_dictionary_item import (
            ChaosParametersDictionaryItem
        )
        from azure.servicefabric.models.chaos_parameters import (
            ChaosParameters
        )
        from azure.servicefabric.models.cluster_health_policy import (
            ClusterHealthPolicy
        )
        from azure.servicefabric.models.chaos_target_filter import (
            ChaosTargetFilter
        )
        from azure.servicefabric.models.chaos_context import (
            ChaosContext
        )

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

        self.assertIsInstance(res[0], ChaosParametersDictionaryItem)
        self.assertEqual(res[0].key, 'myParametersName')
        self.assertIsInstance(res[0].value, ChaosParameters)
        self.assertEqual(res[0].value.time_to_run_in_seconds, '600')
        self.assertEqual(
            res[0].value.max_cluster_stabilization_timeout_in_seconds, 60)
        self.assertEqual(res[0].value.max_concurrent_faults, 1)
        self.assertEqual(res[0].value.enable_move_replica_faults, True)
        self.assertEqual(res[0].value.wait_time_between_faults_in_seconds, 30)
        self.assertEqual(
            res[0].value.wait_time_between_iterations_in_seconds, 15)

        cluster_health_policy = res[0].value.cluster_health_policy
        self.assertIsInstance(cluster_health_policy, ClusterHealthPolicy)
        self.assertEqual(cluster_health_policy.max_percent_unhealthy_nodes, 0)
        self.assertEqual(cluster_health_policy.consider_warning_as_error, True)
        self.assertEqual(
            cluster_health_policy.max_percent_unhealthy_applications, 0)

        self.assertIsInstance(res[0].value.context, ChaosContext)
        self.assertIsInstance(res[0].value.context.map, dict)
        self.assertEqual(
            res[0].value.context.map['myContextKey'], 'myContextValue')

        chaos_target_filter = res[0].value.chaos_target_filter
        self.assertIsInstance(chaos_target_filter, ChaosTargetFilter)
        self.assertIsInstance(
            chaos_target_filter.node_type_inclusion_list, list)
        self.assertEqual(len(chaos_target_filter.node_type_inclusion_list), 2)
        self.assertEqual(
            chaos_target_filter.node_type_inclusion_list[0], 'N0010Ref')
        self.assertEqual(
            chaos_target_filter.node_type_inclusion_list[1], 'N0020Ref')

        self.assertIsInstance(res[1], ChaosParametersDictionaryItem)
        self.assertEqual(res[1].key, 'myOtherParametersName')
        self.assertIsInstance(res[1].value, ChaosParameters)
        self.assertEqual(res[1].value.time_to_run_in_seconds, '300')
        self.assertEqual(
            res[1].value.max_cluster_stabilization_timeout_in_seconds, 20)
        self.assertEqual(res[1].value.max_concurrent_faults, 4)
        self.assertEqual(res[1].value.enable_move_replica_faults, False)
        self.assertEqual(res[1].value.wait_time_between_faults_in_seconds, 50)
        self.assertEqual(
            res[1].value.wait_time_between_iterations_in_seconds, 10)

        cluster_health_policy2 = res[1].value.cluster_health_policy
        self.assertIsInstance(cluster_health_policy2, ClusterHealthPolicy)
        self.assertEqual(cluster_health_policy2.max_percent_unhealthy_nodes, 2)
        self.assertEqual(
            cluster_health_policy2.consider_warning_as_error, False)
        self.assertEqual(
            cluster_health_policy2.max_percent_unhealthy_applications, 5)

        self.assertIsInstance(res[1].value.context, ChaosContext)
        self.assertIsInstance(res[1].value.context.map, dict)
        self.assertEqual(
            res[1].value.context.map['myOtherContextKey'],
            'myOtherContextValue')

        chaos_target_filter2 = res[1].value.chaos_target_filter
        self.assertIsInstance(chaos_target_filter2, ChaosTargetFilter)
        self.assertIsInstance(
            chaos_target_filter2.node_type_inclusion_list, list)
        self.assertEqual(
            len(chaos_target_filter2.node_type_inclusion_list), 2)
        self.assertEqual(
            chaos_target_filter2.node_type_inclusion_list[0],
            'N0030Ref')
        self.assertEqual(
            chaos_target_filter2.node_type_inclusion_list[1],
            'N0040Ref')
