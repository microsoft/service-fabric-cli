# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Telemetry related methods and classes"""

from sys import platform, version
from subprocess import Popen
from datetime import datetime
import inspect
import os
import json
from uuid import uuid4
import portalocker
from knack.log import get_logger
from sfctl.config import get_telemetry_config, get_cli_version_from_pkg
from sfctl.state import increment_telemetry_send_retry_count

# knack CLIConfig has been re-purposed to handle state instead.
SF_CLI_TELEMETRY_NAME = 'sfctl'
# Should not use SF_CLI_TELEMETRY_DIR directly without calling os.path.expanduser first.
SF_CLI_TELEMETRY_DIR = os.path.join('~', '.{0}'.format(SF_CLI_TELEMETRY_NAME))
TELEMETRY_FILE_NAME = 'telemetry'
TELEMETRY_BATCH_CUTOFF = 50  # The number of entries which can be in one telemetry file.
TELEMETRY_FILE_PATH = os.path.expanduser(os.path.join(SF_CLI_TELEMETRY_DIR, TELEMETRY_FILE_NAME))
# Number of consecutive telemetry send failures before retrying only intermittently
TELEMETRY_RETRY_MAX = 5
# After hitting TELEMETRY_RETRY_MAX, how many command calls before retrying telemetry send
TELEMETRY_RETRY_INTERVAL = 50

logger = get_logger(__name__)  # pylint: disable=invalid-name

def check_and_send_telemetry(args_list, invocation_ret_val, exception=None):
    """
    Check if telemetry should be sent, and if so, send the telemetry
    Telemetry should be sent only if the configuration allows for sending telemetry, and if we have
    batched enough data.

    Telemetry will be sent in the background.

    :param args_list: a list of strings, representing the command called along
        with its parameters
    :param invocation_ret_val: (int) The return value of calling invoke on the command in args_list
    :param exception: (str) the string version of the Exception object returned by invoking the
        command in args_list

    :return: None
    """

    # Only send telemetry if user has configured it to be on
    if get_telemetry_config():

        try:

            command_return_tuple = (invocation_ret_val, str(exception))

            command_without_params = []

            # Remove the parameters and keep only the command name
            # Do this by finding the first item which starts with "-"
            for segment in args_list:
                if segment.startswith('-'):
                    break
                command_without_params.append(segment)

            command_as_str = ' '.join(command_without_params)

            # If the commands_without_params is empty, this means that
            # sfctl is called. Don't record this, since it will show up as 'None' in telemetry
            if not command_without_params:
                # Do not send telemetry
                return

            batch_or_send_telemetry(command_as_str, command_return_tuple)

        except:  # pylint: disable=bare-except

            import sys
            ex = sys.exc_info()[0]

            # Allow telemetry to fail silently.

            logger.info(
                str.format('Not sending telemetry because python process due to error: {0}', ex))


def batch_or_send_telemetry(command_as_str, command_return):
    """
    Check if telemetry should be sent or not on the condition of how many entries are
    already batched together. If less than TELEMETRY_BATCH_CUTOFF are in a file, do not
    send telemetry. Add an entry to the file and leave it at that.

    For now, ignore all entries over the initial TELEMETRY_BATCH_CUTOFF count. In the future,
    allow keeping of a few more file (configurable).

    If telemetry should not be sent yet, then do the batching here (write to the file)

    :param command_as_str: string representing a command without the parameters. For example,
        'node list'
    :param command_return: (int, str). int is the returned code,
        str is the error message on command failure.

    :return: (bool, list[str])
        True if should send telemetry. False otherwise.
        If True, the second item in the tuple is a list of strings, with each string representing
        a json object with format of return from get_telemetry_input_as_dict()
    """

    telemetry_json = get_telemetry_input_as_dict(command_return)

    # Open file with mode a+
    # Opens in append and read mode. Pointer is at end of file. Creates new file if files does not
    # exist
    with portalocker.Lock(TELEMETRY_FILE_PATH, timeout=1, fail_when_locked=True, mode='a+') as telemetry_file:  # pylint: disable=line-too-long

        telemetry_file.seek(0)  # Read from the start of the file
        all_lines = telemetry_file.readlines() # This moves pointer back to the end of the file
        total_lines = len(all_lines)

        if total_lines == TELEMETRY_BATCH_CUTOFF - 1:  # Last write to file. Sending telemetry
            telemetry_file.write('{0}, {1}\n'.format(command_as_str, json.dumps(telemetry_json)))
            send_telemetry()
        elif total_lines < TELEMETRY_BATCH_CUTOFF - 1:  # Writing to file. Not sending telemetry
            telemetry_file.write('{0}, {1}\n'.format(command_as_str, json.dumps(telemetry_json)))
        else: # If total lines > TELEMETRY_BATCH_CUTOFF - 1.
            # Not writing to file. Calling send_telemetry
            send_telemetry()


def send_telemetry():
    """
    Send telemetry to the provided instrumentation key. This does not includes a check to
        previously unsent telemetry for offline work.

    We don't want to keep retrying if this keeps failing.
    Increment the telemetry send retry counter in the state file before each attempt.
    Successful telemetry send will reset the counter.
    After the TELEMETRY_RETRY_MAX count, only try sending telemetry every TELEMETRY_RETRY_INTERVAL

    :return: None
    """

    # Mark the start of a telemetry send attempt
    attempt_number = increment_telemetry_send_retry_count()

    # Do not try sending telemetry if we exceed the retry count, and if we are not at the send
    # interval
    if attempt_number > TELEMETRY_RETRY_MAX:
        if ((attempt_number - TELEMETRY_RETRY_MAX) % TELEMETRY_RETRY_INTERVAL) != 0:
            # Don't bother sending telemetry
            logger.info('Not sending telemetry due to too many failed attempts.')
            return
        logger.info('Sending telemetry because retry interval is met.')

    # Get the path of where this file (telemetry.py) is.
    current_file_location = \
        os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

    # This is the absolute path.
    send_telemetry_background_path = \
        os.path.join(current_file_location, 'send_telemetry_background.py')

    # subprocess.run is the newer version of the call command (python 3.5)
    # If you close the terminal, this process will end as well.
    Popen(['python', send_telemetry_background_path], close_fds=True)

    return


def get_telemetry_input_as_dict(command_return):
    """
    Gather the data that needs to be sent along with telemetry

    :param command_return: (int, str). int is the returned code,
        str is the error message on command failure.

    :return: dict
        dict: all values are str
               {'success': call_success,
                'operating_system': platform,
                'python_version': python_version,
                'operation_id': operation_id,
                'error_msg': error_msg,
                'sfctl_version': get_cli_version_from_pkg(),
                'timestamp': time_of_command_call}
    """

    command_return_code = command_return[0]
    command_return_msg = command_return[1]

    call_success = True

    if command_return_code != 0:
        call_success = False

    operation_id = str(uuid4())

    return {'success': str(call_success),
            'operating_system': platform,
            'python_version': version,
            'operation_id': operation_id,
            'error_msg': command_return_msg,
            'sfctl_version': get_cli_version_from_pkg(),
            'timestamp': str(datetime.utcnow())}
