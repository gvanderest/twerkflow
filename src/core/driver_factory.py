from src.core.config_loader import load_settings
from src.drivers.base import TaskService, DocService, PRService
from src.drivers.github_issues import GitHubIssueTaskService
from src.drivers.github_wiki import GitHubWikiDocService
from src.drivers.github_pr import GitHubPRService
from src.drivers.asana import AsanaTaskService
from src.drivers.notion import NotionDocService
from src.drivers.config import GitHubIssueConfig
from github import Github


from pydantic import BaseModel
from typing import Any, Optional


class DriverFactoryConfig(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    settings: Any = None
    task_service_class: Any = GitHubIssueTaskService
    doc_service_class: Any = NotionDocService
    pr_service_class: Any = GitHubPRService
    github_client_class: Any = Github
    config_class: Any = GitHubIssueConfig


class DriverFactory:
    def __init__(self, config: Optional[DriverFactoryConfig] = None):
        config = config or DriverFactoryConfig()
        self.settings = config.settings or load_settings()
        self._task_service_class = config.task_service_class
        self._doc_service_class = config.doc_service_class
        self._pr_service_class = config.pr_service_class
        self._github_client_class = config.github_client_class
        self._config_class = config.config_class

    def get_task_service(self) -> TaskService:
        config = self.settings.get_driver_config("task_service")
        if config.type == "github_issues":
            typed_config = self._config_class(**config.params)
            if not typed_config.token:
                raise ValueError("GITHUB_TOKEN is required")
            github_client = self._github_client_class(
                typed_config.token.get_secret_value()
            )
            repo = github_client.get_repo(typed_config.repo_name)
            return self._task_service_class(repo=repo)
        elif config.type == "asana":
            return AsanaTaskService(**config.params)
        raise ValueError(f"Unknown task driver: {config.type}")

    def get_doc_service(self) -> DocService:
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
        config = self.settings.get_driver_config("pr_service")
        if config.type == "github_pr":
            return self._pr_service_class()
        raise ValueError(f"Unknown pr driver: {config.type}")
