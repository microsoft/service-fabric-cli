"""Azure Service Fabric command line environment for interacting with clusters.

This package contains the following exports:
launch -- main entry point for the command line environment
"""

from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

from sfcli.entry import launch
