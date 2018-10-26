from os import path, pardir
from shutil import rmtree, copytree
import pip

# !Note: The methods in this file depend on the folder structure. Specifically, the methods:
# - get_path_to_readme
# - get_custom_sdk_path

def get_path_to_readme(path_to_root = None):

    # Allow customization of where root should be
    if path_to_root:
        return path.abspath(path.join(path_to_root, 'src', 'README.rst'))

    current_dir = path.dirname(__file__)
    return path.abspath(path.join(current_dir, pardir, 'src', 'README.rst'))


def check_if_should_use_custom_sdk(custom_sdk_path):
    """
    Checks whether or not Travis CI should use a custom service fabric python SDK based on
    <root>/src/README.rst.
    If there are unpublished changes, then we should use the custom SDK if the custom SDK exists.
    Otherwise, use the publicly released python SDK. This ensures that before release, we will
    always test against the newest SDK.

    :param custom_sdk_path: (str) full path to the custom python service fabric SDK
    :return: (bool) Return True if Travis CI should use the service fabric python SDK included
    under <root>/customSDK.
    Return False if TravisCI should use the service fabric python SDK installed from pip.
    """
    sdk_exists = path.isdir(custom_sdk_path)
    if not sdk_exists:
        return False

    path_to_readme = get_path_to_readme()

    with open(path_to_readme, 'r') as readme_file:
        readme_contents = readme_file.read()

        for line in readme_contents.splitlines():
            if line.strip() == 'Unreleased':
                return True

    return False


def replace_public_sdk_with_custom(public_sdk_path, custom_sdk_path):
    """
    Copies the custom SDK to where the public SDK is installed.
    Warning: this method does not do any safety checks before replacing the files.

    :param public_sdk_path: (str) full path to the custom python service fabric SDK
    :param custom_sdk_path: (str) full path to the custom python service fabric SDK
    :return: None
    """

    # empty dir
    dir_to_be_emptied = path.join(public_sdk_path, 'azure', 'servicefabric')
    rmtree(dir_to_be_emptied)

    # copy custom into now empty dir
    copytree(custom_sdk_path, dir_to_be_emptied)


def get_path_public_sdk():
    """
    Gets the full path of the public service fabric python SDK.
    :return: (str) String should always contain a value.
    """

    # Check the location where the service fabric python SDK is installed
    try:
        # pip version 18 (or really, 10+) does not have locations.
        # If this command fails, try something else.
        # pip.locations was an internal command to pip, and has since been removed
        return pip.locations.site_packages
    except:
        # this is a quick and dirty fix. The plan is to deprecate this whole script, so this will do
        return path.dirname(pip.__path__[0])


def get_custom_sdk_path(path_to_root = None):

    # Allow customization of where root should be
    if path_to_root:
        return path.abspath(path.join(path_to_root, 'customSDK', 'servicefabric'))

    current_dir = path.dirname(__file__)
    return path.abspath(path.join(current_dir, pardir, 'customSDK', 'servicefabric'))


def check_and_use_custom_sdk():
    """
    Checks to see if Travis CI should use a custom python service fabric SDK when running
    the tests. If so, update the SDK to the custom one.
    :return: None
    """

    custom_sdk_path = get_custom_sdk_path()

    should_use_custom_sdk = check_if_should_use_custom_sdk(custom_sdk_path)
    if not should_use_custom_sdk:
        return

    print('Updating service fabric python SDK to a custom SDK.')

    # the public sdk path will look something like
    # f:\azure-cli\service-fabric-cli-myfork\env\lib\site-packages
    public_sdk_path = get_path_public_sdk()  # full path

    replace_public_sdk_with_custom(public_sdk_path, custom_sdk_path)


if __name__ == '__main__':
    check_and_use_custom_sdk()
