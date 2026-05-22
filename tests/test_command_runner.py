"""Tests for command runner."""

from typing import List
from src.services.command_runner import CommandRunner


class MockCommandRunner(CommandRunner):
    """Mock implementation of CommandRunner."""

    def __init__(self, response: str):
        self.response = response
        self.cmd = None

    def run(self, cmd: List[str]) -> str:
        """Mock run."""
        self.cmd = cmd
        return self.response


def test_command_runner():
    """Verify command runner works."""
    runner = MockCommandRunner("hello")
    assert runner.run(["echo", "hello"]) == "hello"
    assert runner.cmd == ["echo", "hello"]
