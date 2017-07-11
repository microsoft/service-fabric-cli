"""Help documentation for Service Fabric compose commands."""

from knack.help_files import helps

helps['compose create'] = """
    type: command
    short-summary: Creates a Service Fabric application from a Compose file
    parameters:
        - name: --repo-pass
          type: string
          short-summary: Encrypted contain repository password
"""
