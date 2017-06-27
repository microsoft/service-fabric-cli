"""Azure Service Fabric command line module"""
#!/usr/bin/env python
#
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.

import os
from setuptools import setup


def read(fname):
    """Local read helper function for long documentation"""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='servicefabric_cli',
    version='0.0.1',
    description='Azure Service Fabric command line',
    url='https://github.com/Azure/service-fabric-cli',
    author='Microsoft Corporation',
    author_email='sfpythoncli@microsoft.com',
    license='MIT',
    packages=[
        'azure.servicefabric.cli',
        'tests'
    ],
    long_description=read('README')
)
