# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Azure Service Fabric CLI package that can be installed using setuptools"""

import os
from setuptools import setup


def read(fname):
    """Local read helper function for long documentation"""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='sfctl',
    version='3.1.0',
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
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    keywords='servicefabric azure',
    python_requires='>=2.7,!=3.4,!=3.3,!=3.2,!=3.1,!=3.0,<3.7',
    packages=[
        'sfctl',
        'sfctl.helps',
        'sfctl.tests'
    ],
    install_requires=[
        'knack==0.1.1',
        'msrest>=0.4.4',
        'requests',
        'azure-servicefabric==6.0.2',
        'jsonpickle'
    ],
    extras_require={
        'test': [
            'coverage',
            'nose',
            'pylint',
            'vcrpy',
            'mock'
        ]
    },
    entry_points={
        'console_scripts': ['sfctl=sfctl:launch']
    }
)
