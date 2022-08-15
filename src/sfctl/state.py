# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Read and modify state related to the CLI"""

import os
from datetime import datetime
from knack.config import CLIConfig
from pkg_resources import get_distribution

# knack CLIConfig has all the functionality needed to keep track of state, so we are using that
# here to prevent code duplication. We are using CLIConfig to create a file called 'state' to
# track states associated with SFCTL, such as the last time sfctl version was checked.

# Default names
SF_CLI_NAME = 'sfctl'
SF_CLI_STATE_DIR = os.path.expanduser(os.path.join('~', '.{0}'.format(SF_CLI_NAME)))
STATE_FILE_NAME = 'state'

# Format: Year, month, day, hour, minute, second, microsecond
DATETIME_FORMAT = "Year %Y Month %m Day %d %H:%M:%S:%f"


def get_state_path():
    """
    Returns the path of where the state file of sfctl is stored.
    :return: str
    """

    # This is the same as
    # self.config_path = os.path.join(self.config_dir, CLIConfig._CONFIG_FILE_NAME)
    return CLIConfig(SF_CLI_STATE_DIR, SF_CLI_NAME, 'state').config_path


def get_state_value(name, fallback=None):
    """Gets a state entry by name.
    In the case where the state entry name is not found, will use fallback value."""

    cli_config = CLIConfig(SF_CLI_STATE_DIR, SF_CLI_NAME, 'state')

    return cli_config.get('servicefabric', name, fallback)


def set_state_value(name, value):
    """
    Set a state entry with a specified a value.
    :param name: (str) name of the state
    :param value: (str) value of the state
    :return: None
    """

    cli_config = CLIConfig(SF_CLI_STATE_DIR, SF_CLI_NAME, 'state')
    cli_config.set_value('servicefabric', name, value)


def get_cluster_version_check_time():
    """Get the time that the cluster version was last checked.
    Return as a datetime.datetime object which represents a UTC time, even though timezone is not
    explicitly stated.
    Return None if the value does not exist in state"""

    datetime_str = get_state_value('datetime', None)

    if datetime_str is None:
        return None

    return datetime.strptime(datetime_str, DATETIME_FORMAT)


def set_cluster_version_check_time(custom_time=None):
    """Set the time that the cluster version was last checked.
    Time values are given in UTC, but no timezone information is set.
    If custom_time is not provided, set as the current time in UTC.
    If custom_time is provided, set a custom_time.
    :param custom_time: For testing only. Expects UTC, but without time zone information.
    :type custom_time: datetime.datetime object"""

    if custom_time is None:
        set_state_value('datetime', datetime.utcnow().strftime(DATETIME_FORMAT))
    else:
        set_state_value('datetime', custom_time.strftime(DATETIME_FORMAT))


def get_telemetry_send_retry_count():
    """
    Get the number of send telemetry attempts have failed consecutively.
    :return: int representing number of retries.
             Return None if the value does not exist in state
    """

    telemetry_retry_count_str = get_state_value('telemetry_retry_count', None)

    if telemetry_retry_count_str is None:
        return None

    return int(telemetry_retry_count_str)


def set_telemetry_send_retry_count(retry_count):
    """Set the number of send telemetry attempts have failed consecutively.
    :param retry_count: Number of retries for sending telemetry
    :type retry_count: int"""

    set_state_value('telemetry_retry_count', str(retry_count))


def increment_telemetry_send_retry_count():  # pylint: disable=invalid-name
    """
    Gets the current telemetry send retry count and increments the value by 1.
    If no value is currently set, set the value to 1.
    :return: (int) The new incremented value
    """

    current_retry_count = get_telemetry_send_retry_count()

    if current_retry_count is None:
        set_telemetry_send_retry_count(1)
        return 1

    set_telemetry_send_retry_count(current_retry_count + 1)
    return current_retry_count + 1


def get_sfctl_version():
    """
    Get the version of the sfctl. For example, 6.0.0
    :return: str
    """
    pkg = get_distribution("sfctl")
    return pkg.version
