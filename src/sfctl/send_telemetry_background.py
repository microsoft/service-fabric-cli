# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""A script which sends telemetry in the background as a new process.
This process should end itself in SINGLE_UPLOAD_TIMEOUT seconds for single telemetry calls."""

import sys
from uuid import uuid4
from multiprocessing import Process
from applicationinsights import TelemetryClient
from sfctl.config import get_cli_version_from_pkg

INSTRUMENTATION = '482faeea-c22b-4c75-a1af-5bfe79f36cb7'
SINGLE_UPLOAD_TIMEOUT = 15


def send_telemetry_best_attempt(command_name, telemetry_data):
    """
    Sends telemetry without retry. On failure, telemetry data is lost, and no records are kept.

    :param command_name: (str) the command_name being called, without parameters.
        For example, 'node show'
    :param telemetry_data: (dict) Dict containing the following data, where all inputs are str
        {'success': call_success,
         'operating_system': platform,
         'python_version': python_version,
         'operation_id': operation_id,
         'error_msg': error_msg,
         'sfctl_version': version}

    :return: None
    """

    telemetry_client = TelemetryClient(INSTRUMENTATION)
    # This information is also repeated in telemetry_data for ease of search.
    # This may be moved from one area to another
    telemetry_client.context.application.ver = get_cli_version_from_pkg()

    telemetry_client.track_event(command_name, telemetry_data)

    # This will never end if there is no internet connection, for example.
    telemetry_client.flush()

# pylint: disable=invalid-name
if __name__ == '__main__':

    try:

        command = sys.argv[1]
        call_success = sys.argv[2]
        platform = sys.argv[3]
        python_version = sys.argv[4]
        error_msg = sys.argv[5]

        operation_id = str(uuid4())

        # operation_id is used to ID one instance of a user calling a command.

        telemetry_data_input = {'success': call_success,
                                'operating_system': platform,
                                'python_version': python_version,
                                'operation_id': operation_id,
                                'error_msg': error_msg,
                                'sfctl_version': get_cli_version_from_pkg()}

        # Using a process because we can kill that on a timer. We cannot kill threads the same way.
        telemetry_name = 'sfctl_telemetry'
        send_current_telemetry_process = Process(target=send_telemetry_best_attempt,
                                                 name=telemetry_name,
                                                 args=(command, telemetry_data_input))
        send_current_telemetry_process.name = telemetry_name

        send_current_telemetry_process.start()
        send_current_telemetry_process.join(SINGLE_UPLOAD_TIMEOUT)


        # see if the process is still running. If so, shut down that process
        if send_current_telemetry_process.is_alive():
            send_current_telemetry_process.terminate()

    except:  # pylint: disable=bare-except
        # Developers testing the telemetry code can trace out the error messages here
        # ex = sys.exc_info()[0]
        pass
