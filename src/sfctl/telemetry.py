# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Telemetry related methods and classes"""

from sys import platform, version
from subprocess import Popen
import inspect
import os
import psutil
from knack.log import get_logger
from sfctl.config import get_telemetry_config

# knack CLIConfig has been re-purposed to handle state instead.
SF_CLI_NAME = 'sfctl'
SF_CLI_TELEMETRY_DIR = os.path.join('~', '.{0}'.format(SF_CLI_NAME))
TELEMETRY_FILE_NAME = 'telemetry'

def check_and_send_telemetry(args_list, invocation_ret_val, exception=None):
    """
    Check if telemetry should be sent, and if so, send the telemetry
    Telemetry should be sent only if the configuration allows for sending telemetry and if
    the commandline window does not have too many child processes already running.

    :param args_list: a list of strings, representing the command called along
        with its parameters
    :param invocation_ret_val: (int) The return value of calling invoke on the command in args_list
    :param exception: (str) the string version of the Exception object returned by invoking the
        command in args_list

    :return: None
    """

    logger = get_logger(__name__)

    if get_telemetry_config():

        try:
            # If there are more than 15 python processes, do not create another process
            # (do not send telemetry)
            # len(psutil.Process().parent().children(recursive=True)) does not work, since it is
            # not able to find orphaned children
            python_processes_count = 0

            for process in psutil.process_iter():
                if process.name().find('python') != -1:
                    python_processes_count += 1

            if python_processes_count > 15:
                logger.info('Not sending telemetry because python process count exceeds '
                            'allowable number')
                return

            # In the background, do some work on checking and sending telemetry for the current call
            command_return_tuple = (invocation_ret_val, str(exception))

            send_telemetry(args_list, command_return_tuple)

        except:  # pylint: disable=bare-except

            import sys
            ex = sys.exc_info()[0]

            # Allow telemetry to fail silently.
            logger.info(
                str.format('Not sending telemetry because python process due to error: {0}', ex))


def send_telemetry(command, command_return):
    """
    Send telemetry to the provided instrumentation key. This does not includes a check to
        previously unsent telemetry for offline work.

    :param command: list representing the command which is given, including the parameters.
        For example, ['node', 'list', '--max-results', '10']
    :param command_return: (int, str). int is the returned code,
        str is the error message on command failure.

    :return: None
    """

    command_return_code = command_return[0]
    command_return_msg = command_return[1]

    command_without_params = []

    # Mark commands which retrieve help text (ex. sfctl -h or sfctl node list -h)
    is_help_command = False

    # Remove the parameters and keep only the command name
    # Do this by finding the first item which starts with "-"
    for segment in command:
        if segment in ('-h', '--help'):
            is_help_command = True
        if segment.startswith('-'):
            break
        command_without_params.append(segment)

    # If the commands_without_params is empty, this means that
    # either sfctl is called, or sfctl -h is called. Don't record this.
    # Don't record commands asking for help.
    if is_help_command or not command_without_params:
        # Do not send telemetry
        return

    command_as_str = ' '.join(command_without_params)

    call_success = True

    if command_return_code != 0:
        call_success = False

    # Get the path of where this file (telemetry.py) is.
    abs_send_telemetry_background_root = \
        os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

    abs_send_telemetry_background_path = \
        os.path.join(abs_send_telemetry_background_root, 'send_telemetry_background.py')

    # subprocess.run is the newer version of the call command (python 3.5)
    # If you close the terminal, this process will end as well.
    Popen(['python', abs_send_telemetry_background_path, command_as_str,
           str(call_success), platform, version, command_return_msg], close_fds=True)

    return
