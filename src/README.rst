Service Fabric CLI
==================

A command line interface for interacting with Azure Service Fabric clusters
and their related entities.

Invocation
==========

To get started, after installation run the following:

.. code-block:: bash

  sfctl -h

Change Log
==========

1.2.0rc1
--------

- Updating to Service Fabric 6.0 SDK release candidate
- Added support and testing for Python 3.5, for ease of install on Ubuntu
- Fixing number parsing in command arguments

1.1.0
-----

- Added support for authenticating to clusters with AAD (#10)
- Improved application upload performance (#11)

1.0.1
-----

- Fixed missing helps module.

1.0.0
-----

- Initial release.