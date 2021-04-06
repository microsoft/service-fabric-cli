# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class ProbeExec(Model):
    """Exec command to run inside the container.

    All required parameters must be populated in order to send to Azure.

    :param command: Required. Comma separated command to run inside the
     container for example "sh, -c, echo hello world".
    :type command: str
    """

    _validation = {
        'command': {'required': True},
    }

    _attribute_map = {
        'command': {'key': 'command', 'type': 'str'},
    }

    def __init__(self, *, command: str, **kwargs) -> None:
        super(ProbeExec, self).__init__(**kwargs)
        self.command = command
