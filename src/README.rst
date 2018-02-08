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

4.0.0
-----

- Application provision skeleton added and command removed as part of breaking API change
- Update to 6.1 Service Fabric runtime
- Property command group added
- Added support for external stores when calling application provision
- Provision and unprovision now support no wait return flags
- Application list related commands now support an optional argument to limit the number of results
- Deployed application info can now optionally include health states
- Numerous documentation improvements and corrections
- ChaosContext (context) and ChaosTargetFilter (chaos-target-filter) arguments are added to Chaos start command (#62)

3.0.0
-----

- Rename compose deployment creation and upgrade progress commands to accept 'deployment-name' as identifier (#44)
- Fix incorrect parsing error when updating service description load metrics (#47)
- Fix incorrect application upgrade argument names (#37)

2.0.0
-----

- Update to official 6.0 Service Fabric SDK
- Report cluster health command added
- Report health commands now have an immediate argument to tell the Fabric
  gateway to send the report immediately
- Get cluster configuration and upgrade configuration for stand alone clusters
  commands added
- Added start and update cluster upgrade commands
- Start node command removed (use enable node)
- Stop node command removed (use disable node)
- Added information about new Fabric name hierarchical delimiter (~)
- Health commands now include statistics, can be optionally removed
- Limited set of repair manager commands added
- Infrastructure service commands no longer accept a callback function
- Docker compose commands have had arguments renamed to reflect Service Fabric
  API changes
- Added support to upgrade Docker compose deployments

1.2.0rc2
--------

- Updating to Service Fabric 6.0 SDK release candidate
- Added support and testing for Python 3.5, for ease of install on Ubuntu
- Fixing number parsing in command arguments
- Moving to different versions of pyopenssl and msrest
- Improvement in application upload stability and performance
- Add support for file share upload based on image store connection string

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
