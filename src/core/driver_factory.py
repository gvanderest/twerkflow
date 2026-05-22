"""Provides a factory to instantiate task, document, and PR services."""

from pydantic import BaseModel
from typing import Any, Optional
from src.core.config_loader import load_settings
from src.drivers.base import DocService, PRService, TaskService
from src.drivers.config import GitHubIssueConfig
from src.drivers.github_issues import GitHubIssueTaskService
from src.drivers.github_pr import GitHubPRService
from src.drivers.github_wiki import GitHubWikiDocService
from src.drivers.asana import AsanaTaskService
from src.drivers.notion import NotionDocService
from github import Github


class DriverFactoryConfig(BaseModel):
    """Configuration object for DriverFactory."""

    class Config:
        """Configuration options for Pydantic."""

        arbitrary_types_allowed = True

    settings: Any = None
    task_service_class: Any = GitHubIssueTaskService
    doc_service_class: Any = NotionDocService
    pr_service_class: Any = GitHubPRService
    github_client_class: Any = Github
    config_class: Any = GitHubIssueConfig


class DriverFactory:
    """Factory class to create and configure driver services based on settings."""

    def __init__(self, config: Optional[DriverFactoryConfig] = None):
        """Initializes the DriverFactory."""
        config = config or DriverFactoryConfig()
        self.settings = config.settings or load_settings()
        self._task_service_class = config.task_service_class
        self._doc_service_class = config.doc_service_class
        self._pr_service_class = config.pr_service_class
        self._github_client_class = config.github_client_class
        self._config_class = config.config_class

    def get_task_service(self) -> TaskService:
        """Returns the configured TaskService."""
        config = self.settings.get_driver_config("task_service")
        if config.type == "github_issues":
            typed_config = self._config_class(**config.params)
            if not typed_config.token:
                raise ValueError("GITHUB_TOKEN is required")
            github_client = self._github_client_class(typed_config.token.get_secret_value())
            repo = github_client.get_repo(typed_config.repo_name)
            return self._task_service_class(repo=repo)
        elif config.type == "asana":
            return AsanaTaskService(**config.params)
        raise ValueError(f"Unknown task driver: {config.type}")

    def get_doc_service(self) -> DocService:
        """Returns the configured DocService."""
        config = self.settings.get_driver_config("doc_service")
        if config.type == "github_wiki":
            return GitHubWikiDocService()
        elif config.type == "notion":
            from src.drivers.config import NotionConfig

            typed_config = NotionConfig(**config.params)
            if not typed_config.token:
                raise ValueError("NOTION_API_KEY is required")
            return self._doc_service_class(token=typed_config.token.get_secret_value())
        raise ValueError(f"Unknown doc driver: {config.type}")

    def get_pr_service(self) -> PRService:
        """Returns the configured PRService."""
        config = self.settings.get_driver_config("pr_service")
        if config.type == "github_pr":
            return self._pr_service_class()
        raise ValueError(f"Unknown pr driver: {config.type}")
