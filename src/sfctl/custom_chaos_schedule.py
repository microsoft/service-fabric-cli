# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Custom commands for the Service Fabric chaos schedule test service"""

def parse_time_of_day(time_of_day):
    """
    Parse a TimeOfDay from string.
    time_of_day is a dictionary of
    "Hour": int
    "Minute": int
    """
    from azure.servicefabric.models.time_of_day import TimeOfDay

    if not time_of_day:
        return None

    hour = time_of_day.get("Hour")
    minute = time_of_day.get("Minute")

    if hour is None or minute is None:
        return None

    return TimeOfDay(hour=hour, minute=minute)

def parse_time_range(time_range):
    """
    Parse a TimeRange from string.
    time_range is a dictionary of
    "StartTime": dictionary like time_of_day
    "EndTime": dictionary like time_of_day
    """
    from azure.servicefabric.models.time_range import TimeRange

    if time_range is None:
        return None

    start_time = parse_time_of_day(time_range.get("StartTime"))
    end_time = parse_time_of_day(time_range.get("EndTime"))

    # if either start_time or end_time is None, the resulting API call will fail with an exception

    return TimeRange(start_time=start_time, end_time=end_time)

def parse_active_time_ranges(time_ranges):
    """
    Parse a list of TimeRanges from string.
    time_ranges is a list of dictionaries like time_range
    """

    if time_ranges is None:
        return list()

    parsed_times = list()

    for time_range in time_ranges:
        parsed_times.append(parse_time_range(time_range))

    return parsed_times

def parse_active_days(active_days):
    """
    Parse a ChaosJobActiveDays from string.
    active_days is a dictionary of
    "Sunday": bool,
    ...
    "Saturday": bool
    """
    from azure.servicefabric.models.chaos_schedule_job_active_days_of_week import (
        ChaosScheduleJobActiveDaysOfWeek
    )

    if active_days is None:
        return None

    sunday = active_days.get("Sunday", False)
    monday = active_days.get("Monday", False)
    tuesday = active_days.get("Tuesday", False)
    wednesday = active_days.get("Wednesday", False)
    thursday = active_days.get("Thursday", False)
    friday = active_days.get("Friday", False)
    saturday = active_days.get("Saturday", False)

    return ChaosScheduleJobActiveDaysOfWeek(sunday=sunday,
                                            monday=monday,
                                            tuesday=tuesday,
                                            wednesday=wednesday,
                                            thursday=thursday,
                                            friday=friday,
                                            saturday=saturday)

def parse_job(job):
    """
    Parse a ChaosJob from string.
    job is a dictionary of
    "ChaosParameters": dictionary representing chaos parameters
    "Days": a dictionary like active_days
    "Times": a list like time_ranges
    """
    from azure.servicefabric.models.chaos_schedule_job import (
        ChaosScheduleJob
    )

    if job is None:
        return None

    chaos_parameters = job.get('ChaosParameters')
    active_days = parse_active_days(job.get('Days'))
    times = parse_active_time_ranges(job.get('Times'))

    return ChaosScheduleJob(chaos_parameters=chaos_parameters,
                            days=active_days,
                            times=times)

def parse_jobs(jobs):
    """
    Parse a list of ChaosJobs from string.
    jobs is a list of job
    """

    if jobs is None:
        return list()

    parsed_jobs = list()

    for job in jobs:
        parsed_jobs.append(parse_job(job))

    return parsed_jobs

def parse_chaos_params_dictionary(chaos_parameters_dictionary):
    """
    Parse a list of ChaosParameters dictionary input from string.
    chaos_parameters_dictionary is a list of dictionaries of
    "Key": string
    "Value": a dictionary of a chaos_parameters
    """

    from azure.servicefabric.models.chaos_parameters_dictionary_item import (
        ChaosParametersDictionaryItem
    )

    from sfctl.custom_chaos import (
        parse_chaos_parameters
    )

    if chaos_parameters_dictionary is None:
        return list()

    parsed_dictionary = list()

    for dictionary_entry in chaos_parameters_dictionary:
        key = dictionary_entry.get("Key")
        value = parse_chaos_parameters(dictionary_entry.get("Value"))

        parsed_dictionary.append(ChaosParametersDictionaryItem(key=key, value=value))

    return parsed_dictionary

def set_chaos_schedule( #pylint: disable=too-many-arguments,too-many-locals
        client, version=0,
        start_date_utc='1601-01-01T00:00:00.000Z',
        expiry_date_utc='9999-12-31T23:59:59.999Z',
        chaos_parameters_dictionary=None,
        jobs=None):
    """
    Set the Chaos Schedule currently in use by Chaos.
    Chaos will automatically schedule runs based on the Chaos Schedule.
    """
    from azure.servicefabric.models.chaos_schedule import (
        ChaosSchedule
    )

    if chaos_parameters_dictionary is None:
        chaos_parameters_dictionary = list()

    if jobs is None:
        jobs = list()

    parsed_chaos_params_dictionary = \
        parse_chaos_params_dictionary(chaos_parameters_dictionary)
    parsed_jobs = parse_jobs(jobs)

    schedule = ChaosSchedule(start_date=start_date_utc,
                             expiry_date=expiry_date_utc,
                             chaos_parameters_dictionary=parsed_chaos_params_dictionary,
                             jobs=parsed_jobs)

    return client.post_chaos_schedule(version, schedule)
