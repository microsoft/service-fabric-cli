import pkg_resources

def display_versions(client):
    sfctl_version = pkg_resources.require("sfctl")[0].version
    target_sf_version = pkg_resources.require("azure-servicefabric")[0].version
    print('{version} with target service Fabric version of {target_sf_version}'
          .format(version=sfctl_version, target_sf_version=target_sf_version))
