"""Entry or launch point for Service Fabric CLI.

Handles creating and launching a CLI to handle a user command."""

import os
import sys

from knack import CLI
from .loader import SFCommandLoader, SFCommandHelp

cli_name = 'Azure Service Fabric CLI'
cli_short_name = 'sfcli'

def launch():
    cli_env = CLI(cli_name=cli_name,
                    config_dir=os.path.join('~','.{}'.format(cli_short_name)),
                    config_env_var_prefix=cli_short_name,
                    commands_loader_cls=SFCommandLoader,
                    help_cls=SFCommandHelp)

    return cli_env.invoke(sys.argv[1:])
