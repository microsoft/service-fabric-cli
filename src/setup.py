"""Azure Service Fabric CLI package that can be installed using setuptools"""
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
    name='sf-cli',
    version='unreleased',
    description='Azure Service Fabric command line',
    long_description=read('README.rst'),
    url='https://github.com/Azure/service-fabric-cli',
    author='Microsoft Corporation',
    author_email='sfpythoncli@microsoft.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6'
    ],
    keywords='servicefabric azure',
    python_requires='>=2.7,!=3.5,!=3.4,!=3.3,!=3.2,!=3.1,!=3.0,<3.7',
    packages=[
        'sfcli',
        'sfcli.tests'
    ],
    install_requires=[
        'knack==0.1.1',
        'msrest=~0.4',
        'requests=~2.18',
        'azure-servicefabric==5.6.130'
    ],
    entry_points={
        'console_scripts': ['sfctl=sfcli:launch']
    }
)
 