"""Tests for command runner."""

import subprocess
from typing import List, Optional
from unittest.mock import MagicMock
import pytest
from src.services.command_runner import CommandRunner, SubprocessCommandRunner


class MockCommandRunner(CommandRunner):
    """Mock implementation of CommandRunner."""

    def __init__(self, response: str):
        self.response = response
        self.cmd: Optional[List[str]] = None

    def run(self, cmd: List[str]) -> str:
        """Mock run."""
        self.cmd = cmd
        return self.response


def test_command_runner():
    """Verify command runner works."""
    runner = MockCommandRunner("hello")
    assert runner.run(["echo", "hello"]) == "hello"
    assert runner.cmd == ["echo", "hello"]


def test_subprocess_command_runner():
    """Verify actual subprocess runner."""
    # Mocking the run function directly
    mock_run = MagicMock()
    mock_run.return_value.stdout = "hello\n"

    runner = SubprocessCommandRunner(run_func=mock_run)
    assert runner.run(["echo", "hello"]) == "hello"
    mock_run.assert_called_once()

    # Test error handling
    mock_run_err = MagicMock()
    mock_run_err.side_effect = subprocess.CalledProcessError(1, ["invalid"])

    runner_err = SubprocessCommandRunner(run_func=mock_run_err)
    with pytest.raises(subprocess.CalledProcessError):
        runner_err.run(["invalid"])
