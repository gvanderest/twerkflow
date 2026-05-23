"""Service to run shell commands."""

from abc import ABC, abstractmethod
import subprocess
from typing import List, Callable, Any


class CommandRunner(ABC):
    """Abstract base class for running commands."""

    @abstractmethod
    def run(self, cmd: List[str]) -> str:
        """Runs a command and returns the output."""
        pass


class SubprocessCommandRunner(CommandRunner):
    """Implementation of CommandRunner using subprocess."""

    def __init__(self, run_func: Callable[..., Any] = subprocess.run):
        self.run_func = run_func

    def run(self, cmd: List[str]) -> str:
        """Runs a command and returns the output."""
        result = self.run_func(cmd, capture_output=True, text=True, check=True)
        return str(result.stdout.strip())
