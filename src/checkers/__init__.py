# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

<<<<<<< HEAD:src/checkers/__init__.py
"""Custom PyLint checkers for source"""
=======
VERSION = "6.3.0.9"
>>>>>>> Add custom SDK:customSDK/servicefabric/version.py

from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

from checkers.lca_header import register
