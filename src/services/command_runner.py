"""Service to run shell commands."""

from abc import ABC, abstractmethod
import subprocess
from typing import List


class CommandRunner(ABC):
    """Abstract base class for running commands."""

    @abstractmethod
    def run(self, cmd: List[str]) -> str:
        """Runs a command and returns the output."""
        pass


class SubprocessCommandRunner(CommandRunner):
    """Implementation of CommandRunner using subprocess."""

    def run(self, cmd: List[str]) -> str:
        """Runs a command and returns the output."""
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
