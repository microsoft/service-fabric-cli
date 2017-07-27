# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Entry or launch point for Service Fabric CLI.

Handles creating and launching a CLI to handle a user command."""

import sys

from knack import CLI

from sfctl.config import SF_CLI_CONFIG_DIR, SF_CLI_ENV_VAR_PREFIX, SF_CLI_NAME
from sfctl.commands import SFCommandLoader, SFCommandHelp

def cli():
    """Create CLI environment"""
    return CLI(cli_name=SF_CLI_NAME,
               config_dir=SF_CLI_CONFIG_DIR,
               config_env_var_prefix=SF_CLI_ENV_VAR_PREFIX,
               commands_loader_cls=SFCommandLoader,
               help_cls=SFCommandHelp)

def launch():
    """Entry point for Service Fabric CLI.

    Configures and invokes CLI with arguments passed during the time the python
    session is launched"""

    cli_env = cli()
    return cli_env.invoke(sys.argv[1:])
