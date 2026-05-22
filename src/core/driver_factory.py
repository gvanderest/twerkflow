from src.core.config_loader import load_settings
from src.drivers.base import TaskService, DocService, PRService
from src.drivers.github_issues import GitHubIssueTaskService
from src.drivers.github_wiki import GitHubWikiDocService
from src.drivers.github_pr import GitHubPRService
from src.drivers.asana import AsanaTaskService
from src.drivers.notion import NotionDocService
from github import Github
import os

class DriverFactory:
    def __init__(self):
        self.settings = load_settings()
        self.token = os.getenv("GITHUB_TOKEN")

    def get_task_service(self) -> TaskService:
        config = self.settings.get_driver_config("task_service")
        if config.type == "github_issues":
            if not self.token:
                raise EnvironmentError("GITHUB_TOKEN required for github_issues")
            return GitHubIssueTaskService(config.params["repo_name"], Github(self.token))
        elif config.type == "asana":
            return AsanaTaskService(**config.params)
        raise ValueError(f"Unknown task driver: {config.type}")

    def get_doc_service(self) -> DocService:
        config = self.settings.get_driver_config("doc_service")
        if config.type == "github_wiki":
            return GitHubWikiDocService()
        elif config.type == "notion":
            return NotionDocService()
        raise ValueError(f"Unknown doc driver: {config.type}")

    def get_pr_service(self) -> PRService:
        config = self.settings.get_driver_config("pr_service")
        if config.type == "github_pr":
            return GitHubPRService()
        raise ValueError(f"Unknown pr driver: {config.type}")
