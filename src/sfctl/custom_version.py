import pkg_resources
from knack.util import CLIError

def display_versions(client):
    pkg = pkg_resources.get_distribution("sfctl")
    sfctl_version = pkg.version
    target_sf_version = None
    for dependency in pkg.requires():
        if dependency.key == 'azure-servicefabric':
            # specs is a list of tuples for each version specified
            target_sf_version = dependency.specs[0][1]

    if not target_sf_version:
        raise CLIError('Invalid configuration: dependency of azure-servicefabric is missing')

    print('{0} with target service Fabric version of {1}'.format(sfctl_version, target_sf_version))
