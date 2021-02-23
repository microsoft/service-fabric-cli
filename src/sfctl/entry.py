# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Entry or launch point for Service Fabric CLI.

Handles creating and launching a CLI to handle a user command."""

import sys
from knack.invocation import CommandInvoker
from knack.util import CommandResultItem
from sfctl.config import VersionedCLI
from sfctl.config import SF_CLI_CONFIG_DIR, SF_CLI_ENV_VAR_PREFIX, SF_CLI_NAME
from sfctl.commands import SFCommandLoader, SFCommandHelp
from sfctl.custom_cluster import check_cluster_version
from sfctl.util import is_help_command

def cli():
    """Create CLI environment"""
    return VersionedCLI(cli_name=SF_CLI_NAME,
                        config_dir=SF_CLI_CONFIG_DIR,
                        config_env_var_prefix=SF_CLI_ENV_VAR_PREFIX,
                        invocation_cls=SFInvoker,
                        commands_loader_cls=SFCommandLoader,
                        help_cls=SFCommandHelp)


def launch():
    """Entry point for Service Fabric CLI.

    Configures and invokes CLI with arguments passed during the time the python
    session is launched.

    This is run every time a sfctl command is invoked.

    If you have a local error, say the command is not recognized, then the invoke command will
    raise an exception.
    If you have success, it will return error code 0.
    If the HTTP request returns an error, then an exception is not thrown, and error
    code is not 0."""

    args_list = sys.argv[1:]

    cli_env = cli()

    is_help_cmd = is_help_command(args_list)

    invocation_return_value = cli_env.invoke(args_list)

    # We don't invoke cluster version checking when the user gets an exception, since it means that
    # there is something wrong with their command input, such as missing a required parameter.
    # This is not the same as an error returned from the server, which does not raise an exception.
    # We should also not hit the cluster in the cases of the user inputting a help command (-h)

    if is_help_cmd:
        return invocation_return_value

    try:
        if invocation_return_value != 0 or 'select' in sys.argv[1:]:
            # invocation_return_value is 0 on success
            check_cluster_version(on_failure_or_connection=True)
        else:
            check_cluster_version(on_failure_or_connection=False)

    except:  # pylint: disable=bare-except
        # Catch any exceptions from checking cluster version. For example, if we are not able
        # to read the state file due to corruption, fail silently.
        from knack.log import get_logger
        logger = get_logger(__name__)
        ex = sys.exc_info()[0]
        logger.info('Check cluster version failed due to error: %s', str(ex))

    return invocation_return_value

class SFInvoker(CommandInvoker):  # pylint: disable=too-few-public-methods
    """Extend Invoker to to handle when a system service is not installed (BRS/EventStore cases)."""
    def execute(self, args):
        try:
            return super(SFInvoker, self).execute(args)

        # For exceptions happening while handling http requests, FabricErrorException is thrown with
        # 'Internal Server Error' message, but here we handle the case where gateway is unable
        # to find the service.
        except TypeError:
            if args[0] == 'events':
                from knack.log import get_logger
                logger = get_logger(__name__)
                logger.error('Service is not installed.')
                return CommandResultItem(None, exit_code=0)
            raise
