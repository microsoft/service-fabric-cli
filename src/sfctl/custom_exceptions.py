# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Custom exceptions for Service Fabric CLI"""

class SFCTLInternalException(Exception):
    """ Internal exception indicating that something has gone wrong with sfctl code."""
    def __init__(self, custom_msg):
        super(SFCTLInternalException, self).__init__(custom_msg)
        self.msg = 'SFCTL Internal Error: ' + custom_msg
        self.message = 'SFCTL Internal Error: ' + custom_msg
