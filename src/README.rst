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

Unreleased
----------
- Updated 'application upload' native imagestore application upload to parallelize uploads, greatly reducing overall upload time for applications with many smaller files. Also improved progress log shown by flag '--show-progress'. (#234)

9.0.0
----------
- Added configuration overrides node commands. These commands will be available in the Service fabric runtime 7.0 version (#206)
- Provide option to compress packages on application upload. By default, the newly generated compressed package is deleted after successful upload. (#191)
- Update Create and Update service with new parameter, ServicePlacementTimeLimit (#200)
- Update knack version (#207)

8.0.0
----------
- Update imports for Service fabric runtime version 6.5 (#195)

7.1.0
----------
- Increase default timeout of application upload to 300 seconds, and allow upload timeouts to be configurable. The new timeout will be an overall operation timeout for all uploads, rather than individual operation timeouts of 60 seconds as existed before. Improvements to help text (#131)
- Improve help text on cluster select (#173)
- Add events commands (sfctl events) to retrieve events through EventStore service if installed (#174)
- Cluster select defaults to endpoint http://localhost:19080 if none is provided (#178)
- Change serializers, and change formatting of sfctl container invoke-api output (#179)
- Update Knack version to 0.5.2 (#181)
- Update sfmergeutility version to 0.1.6 (#183)
- Improve error message (#185)

7.0.2
----------
- Pause telemetry collection. Update code for 7.0.2 release (#172)

7.0.1
----------
- Fix bug where an empty directory is generated in the current location. Update code for 7.0.1 release (#167)

7.0.0
----------
- Add upgrade-rollback command for compose deployment (#119)
- Upgrade the knack package dependency to version 0.4.2 (#122)
- Add a check to ensure sfctl version is compatible with the connected cluster version. This check is run periodically and on failures (#123)
- Remove retry on failed commands, such as 500 status codes being returned. This allows the proper error message to propagate through (#125)
- Add Mesh app, volume, service, and service-replica commands (#129)
- Add Mesh network, gateway, code package, secret, and secretvalue commands (#141)
- Allow any Python 3.7.x versions rather than only 3.7.0 (#142)
- Add the command "sfctl mesh deployment create", which takes resource description yaml files as input and deploys the corresponding mesh resources (#146)
- Fix missing option of "Error" health state in health reporting (#151)
- Add telemetry. The following data is collected: Command name without parameters provided or their values, sfctl version, OS, python version, the success or failure of the command, and if the command failed, the error message returned. Upgrade knack package dependency to version 0.5.1 (#152)
- Update to 6.4 Service Fabric runtime (#163)

6.0.1
-----
- Some typo fixes (#115)

6.0.0
-----
- Add application health policies parameter for config upgrade, which are available in Service Fabric runtime 6.3 (#92)
- Add command "sfctl cluster show-connection". Command shows the currently connected cluster connection. Nothing is returned if no endpoint is set (#103)
- Add command override "sfctl --version" to see the current sfctl version (#104)
- Add parameter to set max results for query "sfctl node list" (#113)

5.0.0
-----
- Add commands to get and set chaos schedule (#70)
- Add commands to get chaos and get events for chaos (#70)
- Remove command to get chaos report. The functionality is replaced by command get chaos and the command get chaos events (#70)
- Typo fix for service commands (#71)
- Add missing help text (#71)
- Fix bug in displaying property help text (#71)
- Add scaling policy parameter to the command for service create and the command for service update (#76)
- Add new group called container with commands: invoke-api (invoke raw container REST API) and logs (get container logs) (#82)
- Add support for passing json values to arguments as .txt files. Input starting with '@' are considered paths (#84)
- Update to 6.2 Service Fabric runtime (#97)
- Rename and change value of application upgrade parameter application-name to application-id (#97)

4.0.0
-----

- Update to 6.1 Service Fabric runtime (#64)
- Property command group added
- Added support for external stores when calling application provision
- Provision and unprovision now support no wait return flags
- Application list related commands now support an optional argument to limit the number of results
- Deployed application info can now optionally include health states
- Numerous documentation improvements and corrections
- ChaosContext (context) and ChaosTargetFilter (chaos-target-filter) arguments are added to Chaos start command (#62)
- Add test structure to verify correct HTTP request generation
- Update provision application type command to match the latest Service Fabric runtime, now a custom command
- Add command to get container logs deployed on node

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
