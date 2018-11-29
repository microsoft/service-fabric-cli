# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Commands to configure settings in sfctl"""

from knack.util import CLIError
from sfctl.config import set_telemetry_config

def set_telemetry(on=False, off=False):  # pylint: disable=invalid-name
    """Turn telemetry on or off."""

    # Check that both properties are not set to the same thing
    if on == off:
        raise CLIError('Only one of --on or --off should be set.')

    if on:
        set_telemetry_config(True)
        print('Telemetry has been turned on')
    else:
        set_telemetry_config(False)
        print('Telemetry has been turned off')
