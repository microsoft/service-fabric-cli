# coding=utf-8
# --------------------------------------------------------------------------
#
# Copyright (c) Microsoft Corporation. All rights reserved.
#
# The MIT License (MIT)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the ""Software""), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED *AS IS*, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#
# --------------------------------------------------------------------------

# This file is used for handwritten extensions to the generated code. Example:
# https://github.com/Azure/azure-sdk-for-python/blob/main/doc/dev/customize_code/how-to-patch-sdk-code.md
def patch_sdk():
    pass

# from ._service_fabric_client_apis import ServiceFabricClientAPIs as ServiceClientGenerated
# from azure.core.pipeline import PipelineRequest
# from azure.core.pipeline.policies import SansIOHTTPPolicy

# class MyAuthenticationPolicy(SansIOHTTPPolicy):

#     def __init__(self, key: str):
#         self.key = key

#     def on_request(self, request: PipelineRequest):
#         # request.http_request.headers["Authorization"] = f"My key is {self.key}"
#         return super().on_request(request)

# class ServiceClient(ServiceClientGenerated):

#     def __init__(self, endpoint: str, credential: str, **kwargs):
#         super().__init__(
#             endpoint=endpoint,
#             credential=credential,
#             authentication_policy=kwargs.pop("authentication_policy", MyAuthenticationPolicy(credential)),
#             **kwargs
#         )

# __all__ = ["ServiceClient"]