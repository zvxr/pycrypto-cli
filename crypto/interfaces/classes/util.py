
import getpass
import os
import subprocess

"""Utility (helper) methods for commandline functionality.
"""

def get_data_from_clipboard():
    """Returns what is in the clipboard."""
    process = subprocess.Popen(['pbpaste'], stdout=subprocess.PIPE, close_fds=True)
    stdout, stderr = process.communicate()
    return stdout.decode('utf-8')


def get_key():
    """Get and return key using getpass."""
    return getpass.getpass("Please enter key: ")


def store_data_in_clipboard(data):
    """Store data in clipboard."""
    process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
    stdoutdata, stderrdata = process.communicate(input=data.encode('utf-8'))


def wait_on_exit(message="Press ENTER key or CTRL+C to complete."):
    raw_input(message)
