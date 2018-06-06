import pkg_resources

def display_versions(client):
    pkg = pkg_resources.get_distribution("sfctl")
    sfctl_version = pkg.version
    target_sf_version = None
    for dependency in pkg.requires():
        if dependency.key == 'azure-servicefabric':
            # specs is a list of tuples for each version specified
            target_sf_version = dependency.specs[0][1]

    print('{version} with target service Fabric version of {target_sf_version}'
          .format(version=sfctl_version, target_sf_version=target_sf_version))
