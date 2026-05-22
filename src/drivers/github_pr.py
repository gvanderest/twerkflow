"""Provides a service to interact with GitHub Pull Requests."""

from src.drivers.base import PRService


class GitHubPRService(PRService):
    """Service to interact with GitHub Pull Requests."""

    def create_pr(self, branch: str, title: str, description: str) -> str:
        """Creates a Pull Request on GitHub."""
        raise NotImplementedError("GitHubPRService.create_pr not implemented")
