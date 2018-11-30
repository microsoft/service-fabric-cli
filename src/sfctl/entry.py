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
from sfctl.custom_cluster import check_cluster_version
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
    session is launched.

    This is run every time a sfctl command is invoked."""

    args_list = sys.argv[1:]

    cli_env = cli()

    invoke_return_value = None

    try:
        invoke_return_value = cli_env.invoke(args_list)
        check_and_send_telemetry(args_list, invoke_return_value, cli_env.result.error)

    # Cannot use except BaseException until python 2.7 support is dropped
    except:  # pylint: disable=bare-except
        ex = sys.exc_info()[0]

        # We don't get a very useful message from SystemExit, which are the errors which are
        # returned locally to the user, for example, if the command doesn't exist in sfctl.
        check_and_send_telemetry(args_list, -1, str(ex))

        # Log the exception and pass it back to the user
        raise

    try:
        if invoke_return_value != 0 or ('cluster' and 'select' in sys.argv[1:]):
            # invoke_return_value is 0 on success
            check_cluster_version(on_failure_or_connection=True, dummy_cluster_version='invalid')
        else:
            check_cluster_version(on_failure_or_connection=False, dummy_cluster_version='invalid')

    except:  # pylint: disable=bare-except
        # Catch any exceptions from checking cluster version. For example, if we are not able
        # to read the state file due to corruption, fail silently.
        from knack.log import get_logger
        logger = get_logger(__name__)
        ex = sys.exc_info()[0]
        logger.info('Check cluster version failed due to error: %s', str(ex))

    return invoke_return_value
