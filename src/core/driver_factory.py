from src.core.config_loader import load_settings
from src.drivers.base import TaskService, DocService, PRService
from src.drivers.github_issues import GitHubIssueTaskService
from src.drivers.github_wiki import GitHubWikiDocService
from src.drivers.github_pr import GitHubPRService
from src.drivers.asana import AsanaTaskService
from src.drivers.notion import NotionDocService
from src.drivers.config import GitHubIssueConfig
from github import Github
import os

class DriverFactory:
    def __init__(self):
        self.settings = load_settings()

    def get_task_service(self) -> TaskService:
        config = self.settings.get_driver_config("task_service")
        if config.type == "github_issues":
            typed_config = GitHubIssueConfig(**config.params)
            github_client = Github(typed_config.token.get_secret_value())
            repo = github_client.get_repo(typed_config.repo_name)
            return GitHubIssueTaskService(repo=repo)
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
            return NotionDocService(token=typed_config.token.get_secret_value())
        raise ValueError(f"Unknown doc driver: {config.type}")

    def get_pr_service(self) -> PRService:
        config = self.settings.get_driver_config("pr_service")
        if config.type == "github_pr":
            return GitHubPRService()
        raise ValueError(f"Unknown pr driver: {config.type}")
