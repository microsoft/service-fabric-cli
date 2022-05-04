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

    if not time_of_day:
        return None

    hour = time_of_day.get("Hour")
    minute = time_of_day.get("Minute")

    if hour is None or minute is None:
        return None

    return {"Hour": hour, "Minute": minute}


def parse_time_range(time_range):
    """
    Parse a TimeRange from string.
    time_range is a dictionary of
    "StartTime": dictionary like time_of_day
    "EndTime": dictionary like time_of_day
    """
    if time_range is None:
        return None

    start_time = parse_time_of_day(time_range.get("StartTime"))
    end_time = parse_time_of_day(time_range.get("EndTime"))

    # if either start_time or end_time is None, the resulting API call will fail with an exception

    return {"StartTime": start_time, "EndTime": end_time}

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

    if active_days is None:
        return None

    sunday = active_days.get("Sunday", False)
    monday = active_days.get("Monday", False)
    tuesday = active_days.get("Tuesday", False)
    wednesday = active_days.get("Wednesday", False)
    thursday = active_days.get("Thursday", False)
    friday = active_days.get("Friday", False)
    saturday = active_days.get("Saturday", False)

    return {"Sunday": sunday,
            "Monday": monday,
            "Tuesday": tuesday,
            "Wednesday": wednesday,
            "Thursday": thursday,
            "Friday": friday,
            "Saturday": saturday}


def parse_job(job):
    """
    Parse a ChaosJob from string.
    job is a dictionary of
    "ChaosParameters": dictionary representing chaos parameters
    "Days": a dictionary like active_days
    "Times": a list like time_ranges
    """

    if job is None:
        return None

    chaos_parameters = job.get('ChaosParameters')
    active_days = parse_active_days(job.get('Days'))
    times = parse_active_time_ranges(job.get('Times'))

    return {"ChaosParameters": chaos_parameters,
            "Days": active_days,
            "Times": times}

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
    from sfctl.custom_chaos import parse_chaos_parameters

    if chaos_parameters_dictionary is None:
        return list()

    parsed_dictionary = list()

    for dictionary_entry in chaos_parameters_dictionary:
        key = dictionary_entry.get("Key")
        value = parse_chaos_parameters(dictionary_entry.get("Value"))

        parsed_dictionary.append({"Key": key, "Value": value})

    return parsed_dictionary

def set_chaos_schedule( #pylint: disable=too-many-arguments,too-many-locals
        client, version=0,
        start_date_utc='1601-01-01T00:00:00.000Z',
        expiry_date_utc='9999-12-31T23:59:59.999Z',
        chaos_parameters_dictionary=None,
        jobs=None,
        timeout=60):
    """
    Set the Chaos Schedule currently in use by Chaos.
    Chaos will automatically schedule runs based on the Chaos Schedule.
    """

    if chaos_parameters_dictionary is None:
        chaos_parameters_dictionary = list()

    if jobs is None:
        jobs = list()

    parsed_chaos_params_dictionary = \
        parse_chaos_params_dictionary(chaos_parameters_dictionary)
    parsed_jobs = parse_jobs(jobs)

    schedule = {"StartDate": start_date_utc,
                "ExpiryDate": expiry_date_utc,
                "ChaosParametersDictionary": parsed_chaos_params_dictionary,
                "Jobs": parsed_jobs,
                "Version": version}

    return client.post_chaos_schedule(schedule, timeout=timeout)
