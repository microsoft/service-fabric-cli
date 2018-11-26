# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Read and modify state related to the CLI"""

import os
from datetime import datetime, timezone
from knack.config import CLIConfig
from pkg_resources import get_distribution

# knack CLIConfig has all the functionality needed to keep track of state, so we are using that
# here to prevent code duplication. We are using CLIConfig to create a file called 'state' to
# track stats associated with SFCTL, such as the last time sfctl version was checked.

# Default names
SF_CLI_NAME = 'sfctl'
SF_CLI_STATE_DIR = os.path.join('~', '.{0}'.format(SF_CLI_NAME))
STATE_FILE_NAME = 'state'

# Format: Year, month, day, hour, minute, second, microsecond, timezone
DATETIME_FORMAT = "Year %Y Month %m Day %d %H:%M:%S:%f %Z"


def get_state_path():

    return CLIConfig(SF_CLI_STATE_DIR, SF_CLI_NAME, 'state').config_path


def get_state_value(name, fallback=None):
    """Gets a state entry by name.

    In the case where the state entry name is not found, will use fallback value."""

    cli_config = CLIConfig(SF_CLI_STATE_DIR, SF_CLI_NAME, 'state')

    return cli_config.get('servicefabric', name, fallback)


def set_state_value(name, value):
    """Set a state entry to a value."""

    cli_config = CLIConfig(SF_CLI_STATE_DIR, SF_CLI_NAME, 'state')
    cli_config.set_value('servicefabric', name, value)


def get_cluster_version_check_time():
    """Get the time that the cluster version was last checked.
    Return as a datetime.datetime object which represents a UTC time."""

    datetime_str = get_state_value('datetime', None)
    return datetime.strptime(datetime_str, DATETIME_FORMAT)


def set_cluster_version_check_time(custom_time=None):
    """Set the time that the cluster version was last checked. Set as the current time in UTC.

    :param custom_time: For testing only. Expects UTC
    :type custom_time: datetime.datetime object"""

    if custom_time is None:
        set_state_value('datetime', datetime.now(timezone.utc).strftime(DATETIME_FORMAT))
    else:
        set_state_value('datetime', custom_time.strftime(DATETIME_FORMAT))


def get_sfctl_version():
    pkg = get_distribution("sfctl")
    return pkg.version
