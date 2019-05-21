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

from .diagnostics_sink_properties import DiagnosticsSinkProperties


class AzureInternalMonitoringPipelineSinkDescription(DiagnosticsSinkProperties):
    """Diagnostics settings for Geneva.

    :param name: Name of the sink. This value is referenced by
     DiagnosticsReferenceDescription
    :type name: str
    :param description: A description of the sink.
    :type description: str
    :param kind: Constant filled by server.
    :type kind: str
    :param account_name: Azure Internal monitoring pipeline account.
    :type account_name: str
    :param namespace: Azure Internal monitoring pipeline account namespace.
    :type namespace: str
    :param ma_config_url: Azure Internal monitoring agent configuration.
    :type ma_config_url: str
    :param fluentd_config_url: Azure Internal monitoring agent fluentd
     configuration.
    :type fluentd_config_url: str
    :param auto_key_config_url: Azure Internal monitoring pipeline autokey
     associated with the certificate.
    :type auto_key_config_url: str
    """

    _validation = {
        'kind': {'required': True},
    }

    _attribute_map = {
        'name': {'key': 'name', 'type': 'str'},
        'description': {'key': 'description', 'type': 'str'},
        'kind': {'key': 'kind', 'type': 'str'},
        'account_name': {'key': 'accountName', 'type': 'str'},
        'namespace': {'key': 'namespace', 'type': 'str'},
        'ma_config_url': {'key': 'maConfigUrl', 'type': 'str'},
        'fluentd_config_url': {'key': 'fluentdConfigUrl', 'type': 'str'},
        'auto_key_config_url': {'key': 'autoKeyConfigUrl', 'type': 'str'},
    }

    def __init__(self, name=None, description=None, account_name=None, namespace=None, ma_config_url=None, fluentd_config_url=None, auto_key_config_url=None):
        super(AzureInternalMonitoringPipelineSinkDescription, self).__init__(name=name, description=description)
        self.account_name = account_name
        self.namespace = namespace
        self.ma_config_url = ma_config_url
        self.fluentd_config_url = fluentd_config_url
        self.auto_key_config_url = auto_key_config_url
        self.kind = 'AzureInternalMonitoringPipeline'
