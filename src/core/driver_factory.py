from typing import Dict, Type
from src.core.config_loader import load_settings
from src.drivers.base import TaskService, DocService, PRService
from src.drivers.github_issues import GitHubIssueTaskService
from src.drivers.github_wiki import GitHubWikiDocService
from src.drivers.github_pr import GitHubPRService
from src.drivers.asana import AsanaTaskService
from src.drivers.notion import NotionDocService

# Mapping driver types to implementation classes
TASK_DRIVERS = {
    "github_issues": GitHubIssueTaskService,
    "asana": AsanaTaskService,
}

DOC_DRIVERS = {
    "github_wiki": GitHubWikiDocService,
    "notion": NotionDocService,
}

PR_DRIVERS = {
    "github_pr": GitHubPRService,
}

class DriverFactory:
    def __init__(self):
        self.settings = load_settings()

    def get_task_service(self) -> TaskService:
        config = self.settings.get_driver_config("task_service")
        driver_cls = TASK_DRIVERS[config.type]
        # In a real setup, we'd pass config.params to the constructor
        return driver_cls(**config.params)

    def get_doc_service(self) -> DocService:
        config = self.settings.get_driver_config("doc_service")
        driver_cls = DOC_DRIVERS[config.type]
        return driver_cls(**config.params)

    def get_pr_service(self) -> PRService:
        config = self.settings.get_driver_config("pr_service")
        driver_cls = PR_DRIVERS[config.type]
        return driver_cls(**config.params)
