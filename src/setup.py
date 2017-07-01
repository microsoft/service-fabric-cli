"""Azure Service Fabric CLI module that can be installed using setuptools"""
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
    version='1.0.0.dev1',
    description='Azure Service Fabric command line',
    long_description=read('README.rst'),
    url='https://github.com/Azure/service-fabric-cli',
    author='Microsoft Corporation',
    author_email='sfpythoncli@microsoft.com',
    license='MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: User Interfaces'
    ],
    keywords='servicefabric azure',
    python_requires='>=3',
    packages=[
        'azure.servicefabric.cli'
    ],
    install_requires=[
        'knack'
    ],
    entry_points={
        'console_scripts': ['sf=azure.servicefabric.cli.command_line:launch']
    }
)
