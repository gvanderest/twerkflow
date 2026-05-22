import os
import pytest

def pytest_configure(config):
    """
    Cleans the process environment before any tests are collected.
    This prevents accidental leakage of host-machine credentials.
    """
    # Forcefully remove sensitive variables
    os.environ.pop("GITHUB_TOKEN", None)
