# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Custom PyLint checkers for source"""

from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

from checkers.lca_header import register
