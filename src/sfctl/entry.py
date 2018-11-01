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

    cli_env = cli()
    invoke_return_value = cli_env.invoke(sys.argv[1:])

    if invoke_return_value != 0 or ('cluster' and 'select' in sys.argv[1:]):
        check_cluster_version(on_failure_or_connection=True, dummy_cluster_version='invalid')
    else:
        check_cluster_version(on_failure_or_connection=False, dummy_cluster_version='invalid')

    return invoke_return_value
