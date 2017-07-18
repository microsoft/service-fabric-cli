"""Custom parameter handling for commands"""
import json
from knack.arguments import ArgumentsContext

def json_encoded(arg_str):
    """Convert from argument JSON string to complex object"""

    return json.loads(arg_str)

def custom_arguments(self, _):
    """Load specialized arguments for commands"""

    # Global argument
    with ArgumentsContext(self, '') as arg_context:
        arg_context.argument('timeout', type=int, default=60,
                             options_list=('-t', '--timeout'),
                             help='Server timeout in seconds')

    with ArgumentsContext(self, 'application create') as arg_context:
        arg_context.argument('parameters', type=json_encoded)
        arg_context.argument('metrics', type=json_encoded)

    with ArgumentsContext(self, 'application upgrade') as arg_context:
        arg_context.argument('parameters', type=json_encoded)
        arg_context.argument('default_service_health_policy',
                             type=json_encoded)
        arg_context.argument('service_health_policy', type=json_encoded)

    with ArgumentsContext(self, 'chaos start') as arg_context:
        arg_context.argument('app_type_health_policy_map', type=json_encoded)
