import getpass
import os
import subprocess


"""Utility (helper) methods for commandline functionality.
"""

def get_key():
    """Get and return key using getpass."""
    return getpass.getpass("Please enter key: ")
