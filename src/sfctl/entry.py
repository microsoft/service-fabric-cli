# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Entry or launch point for Service Fabric CLI.

Handles creating and launching a CLI to handle a user command."""

import sys
from sfctl.config import VersionedCLI
from sfctl.config import SF_CLI_CONFIG_DIR, SF_CLI_ENV_VAR_PREFIX, SF_CLI_NAME
from sfctl.commands import SFCommandLoader, SFCommandHelp
from sfctl.telemetry import check_and_send_telemetry


def cli():
    """Create CLI environment"""
    return VersionedCLI(cli_name=SF_CLI_NAME,
                        config_dir=SF_CLI_CONFIG_DIR,
                        config_env_var_prefix=SF_CLI_ENV_VAR_PREFIX,
                        commands_loader_cls=SFCommandLoader,
                        help_cls=SFCommandHelp)


def launch():
    """Entry point for Service Fabric CLI.

    Configures and invokes CLI with arguments passed during the time the python
    session is launched"""

    args_list = sys.argv[1:]

    cli_env = cli()

    try:
        invocation_ret_val = cli_env.invoke(args_list)
        check_and_send_telemetry(args_list, invocation_ret_val, cli_env.result.error)

    except:  # Cannot use except BaseException until python 2.7 support is dropped
        ex = sys.exc_info()[0]

        # We don't get a very useful message from SystemExit, which are the errors which are
        # returned locally to the user, for example, if the command doesn't exist in sfctl.
        check_and_send_telemetry(args_list, -1, str(ex))

        # Log the exception and pass it back to the user
        raise

    return invocation_ret_val