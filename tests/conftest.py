import os
import pytest
import socket

def pytest_configure(config):
    """
    Cleans the process environment before any tests are collected.
    This prevents accidental leakage of host-machine credentials.
    """
    # Forcefully remove sensitive variables
    os.environ.pop("GITHUB_TOKEN", None)

@pytest.fixture(autouse=True)
def block_network(monkeypatch):
    """
    Blocks all network access during tests.
    Any attempt to use the network will raise a RuntimeError.
    """
    def block(*args, **kwargs):
        raise RuntimeError("Network access is blocked during tests! You must mock external calls.")

    monkeypatch.setattr(socket, "socket", block)
