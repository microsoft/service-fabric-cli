# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""A script which sends telemetry in the background as a new process.
This process should end itself in SINGLE_UPLOAD_TIMEOUT seconds for single telemetry calls."""

import os
import json
from multiprocessing import Process
import portalocker
from applicationinsights import TelemetryClient
from sfctl.telemetry import TELEMETRY_FILE_PATH
from sfctl.state import set_telemetry_send_retry_count

INSTRUMENTATION = '482faeea-c22b-4c75-a1af-5bfe79f36cb7'
SINGLE_UPLOAD_TIMEOUT = 30

def read_telemetry_entries():
    """
    Read and return the telemetry entries.

    :return: List[(str, dict)] returns a list of tuples representing the input
        to the track_event command for the application insights telemetry client.
        Each tuple contains the following:
            (str) the command_name being called, without parameters. For example, 'node show'
            (dict) See return from get_telemetry_input_as_dict()
    """

    return_tuples = []

    # Mode r starts at the beginning of the file
    with portalocker.Lock(TELEMETRY_FILE_PATH, timeout=1, fail_when_locked=True, mode='r') as telemetry_file:  # pylint: disable=line-too-long
        all_lines = telemetry_file.readlines()

        # Parse the lines. The lines have format {0}, {1}
        for line in all_lines:
            if line.strip():  # ignore any empty lines
                index_of_first_comma = line.find(',')
                command_name = line[:index_of_first_comma]
                json_string = line[index_of_first_comma+1:]
                telemetry_dict = json.loads(json_string)
                return_tuples.append((command_name, telemetry_dict))

    return return_tuples


def send_telemetry_best_attempt():
    """
    Sends telemetry data from file TELEMETRY_FILE_PATH. The data is preserved if the process
    is terminated before telemetry is sent, since removal of the TELEMETRY_FILE_PATH is called
    only once that is completed.

    There is a possibility of duplicate data, since if the telemetry data is sent out, and the
    process is terminated before the file is deleted, we may end up resending.
    This is acceptable since it will be rare, and since we have unique IDs for each telemetry
    event.

    There is a possibility that the process is terminated after telemetry send and file delete,
    but before we can resent the telemetry send retry counter. This case will also be rare.
    It will also take care of itself over time, since we will keep filling up new data, and
    eventually it will send. We may lose some data, but that can be fixed in future changes.

    We are also not currently setting time on the telemetry. We are counting the time as the time
    sent. There is an entry to track the time, but the default sorting will not work with time
    necessarily. We accept this right now, since there is not much we do with time data.

    :return: None
    """

    telemetry_tuples = read_telemetry_entries()

    telemetry_client = TelemetryClient(INSTRUMENTATION)

    for tup in telemetry_tuples:
        telemetry_client.track_event(tup[0], tup[1])

    # This will never end if there is no internet connection, for example.
    telemetry_client.flush()

    # After send has completed, delete the file
    try:
        os.remove(TELEMETRY_FILE_PATH)
    except:  # pylint: disable=bare-except
        pass

    # After send has completed, clear the telemetry retry counter
    set_telemetry_send_retry_count(0)

# pylint: disable=invalid-name
if __name__ == '__main__':

    try:
        # Using a process because we can kill that on a timer. We cannot kill threads the same way.
        telemetry_name = 'sfctl_telemetry'
        send_current_telemetry_process = Process(target=send_telemetry_best_attempt,
                                                 name=telemetry_name)

        send_current_telemetry_process.start()
        send_current_telemetry_process.join(SINGLE_UPLOAD_TIMEOUT)


        # see if the process is still running. If so, shut down that process
        if send_current_telemetry_process.is_alive():
            send_current_telemetry_process.terminate()

    except:  # pylint: disable=bare-except
        # Developers testing the telemetry code can trace out the error messages here
        # ex = sys.exc_info()[0]
        pass
