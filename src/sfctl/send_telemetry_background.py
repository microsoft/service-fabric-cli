# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""A script which sends telemetry in the background as a new process.
This process should end itself in SINGLE_UPLOAD_TIMEOUT seconds for single telemetry calls."""

import sys
from applicationinsights import TelemetryClient
from uuid import uuid4
from multiprocessing import Process
from sfctl.config import get_cli_version_from_pkg

instrumentation_key = '5b9ab102-e26b-4b75-919e-f448c521ff11'
SINGLE_UPLOAD_TIMEOUT = 15


def send_telemetry_best_attempt(command, telemetry_data):

    tc = TelemetryClient(instrumentation_key)
    # This information is also repeated in telemetry_data for ease of search.
    # This may be moved from one area to another
    tc.context.application.ver = get_cli_version_from_pkg()

    tc.track_event(command, telemetry_data)

    # This will never end if there is no internet connection, for example.
    tc.flush()


if __name__ == '__main__':

    try:

        command = sys.argv[1]
        call_success  = sys.argv[2]
        platform = sys.argv[3]
        python_version = sys.argv[4]
        error_msg = sys.argv[5]

        operation_id = str(uuid4())

        # operation_id is used to ID one instance of a user calling a command.

        telemetry_data = {'success': call_success,
                          'operating_system': platform,
                          'python_version': python_version,
                          'operation_id': operation_id,
                          'error_msg': error_msg,
                          'sfctl_version': get_cli_version_from_pkg()}

        # Using a process because we can kill that on a timer. We cannot kill threads the same way.
        telemetry_name = 'sfctl_telemetry'
        send_current_telemetry_process = Process(target=send_telemetry_best_attempt,
                                                 name=telemetry_name,
                                                 args=(command, telemetry_data))
        send_current_telemetry_process.name = telemetry_name

        send_current_telemetry_process.start()
        send_current_telemetry_process.join(SINGLE_UPLOAD_TIMEOUT)


        # see if the process is still running. If so, shut down that process
        if send_current_telemetry_process.is_alive():
            send_current_telemetry_process.terminate()

    except:
        # Developers testing the telemetry code can trace out the error messages here
        # ex = sys.exc_info()[0]
        pass