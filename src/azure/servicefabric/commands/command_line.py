"""Entry or launch point for Service Fabric CLI.

Handles creating and launching a CLI to handle a user command."""

import os
import sys

from knack import CLI
from .loader import SFCommandLoader, SFCommandHelp

SF_CLI_NAME = 'Azure Service Fabric CLI'
SF_CLI_SHORT_NAME = 'sfcli'


def launch():
    """Entry point for Service Fabric CLI.

    Configures and invokes CLI with arguments passed during the time the python
    session is launched"""

    cli_env = CLI(cli_name=SF_CLI_NAME,
                  config_dir=os.path.join('~',
                                          '.{}'.format(SF_CLI_SHORT_NAME)),
                  config_env_var_prefix=SF_CLI_SHORT_NAME,
                  commands_loader_cls=SFCommandLoader,
                  help_cls=SFCommandHelp)

    return cli_env.invoke(sys.argv[1:])
