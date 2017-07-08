"""General helper functions for Azure Service Fabric CLI"""

def get_pass(prompt="Password: "):
    """Prompt user for secure password input"""
    import getpass
    return getpass.getpass(prompt)