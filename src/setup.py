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
    version='11.2.1',
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
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10'
    ],
    keywords='servicefabric azure',
    python_requires='>3.8, <4',
    packages=[
        'sfctl',
        'sfctl.helps',
        'sfctl.tests'
    ],
    install_requires=[
        'knack==0.6.3',
        'requests==2.32.3',
        'msrest>=0.5.0',
        'msrestazure',
        'azure-servicefabric==8.2.0.0',
        'adal',
        'future',
        'applicationinsights',
        'psutil',
        'portalocker',
        'six',
        "joblib==1.4.2",
        "tqdm"
    ],
    extras_require={
        'test': [
            'coverage',
            'nose2',
            'pylint==2.7.2',
            'vcrpy',
            'mock',
            'contextlib2',
        ]
    },
    entry_points={
        'console_scripts': ['sfctl=sfctl:launch']
    }
)
