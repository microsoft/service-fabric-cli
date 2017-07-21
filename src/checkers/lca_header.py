# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Checkers to verify LCA header compliance"""

from pylint.checkers import BaseChecker
from pylint.interfaces import IRawChecker

class LCAHeaderChecker(BaseChecker):
    """Check that files will always start with the required Microsoft LCA
    header"""

    __implements__ = IRawChecker

    name = 'ms-header'
    priority = -1
    msgs = {
        'W5001': (
            'Missing copyright header',
            'missing-ms-header',
            'All source files should contain Microsoft copyright header.'
        ),
    }
    options = ()

    def process_module(self, node):
        """process a module
        the module's content is accessible via node.stream() function
        """

        legal_copyright = ('Copyright (c) Microsoft Corporation. '
                           'All rights reserved.')

        with node.stream() as stream:
            for (lineno, line) in enumerate(stream):
                if line.lstrip().startswith('#'):
                    if legal_copyright in line:
                        return
                elif not line.lstrip():
                    continue
                else:
                    self.add_message('missing-ms-header', line=lineno)
                    return

def register(linter):
    """required method to auto register this checker"""
    linter.register_checker(LCAHeaderChecker(linter))
