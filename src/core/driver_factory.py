from src.core.config_loader import load_settings
from src.drivers.base import TaskService, DocService, PRService
from src.drivers.github_issues import GitHubIssueTaskService
from src.drivers.github_wiki import GitHubWikiDocService
from src.drivers.github_pr import GitHubPRService
from src.drivers.asana import AsanaTaskService
from src.drivers.notion import NotionDocService
from src.drivers.config import GitHubIssueConfig
from github import Github


class DriverFactory:
    def __init__(
        self,
        settings=None,
        task_service_class=GitHubIssueTaskService,
        doc_service_class=NotionDocService,
        pr_service_class=GitHubPRService,
        github_client_class=Github,
        config_class=GitHubIssueConfig,
    ):
        self.settings = settings or load_settings()
        self._task_service_class = task_service_class
        self._doc_service_class = doc_service_class
        self._pr_service_class = pr_service_class
        self._github_client_class = github_client_class
        self._config_class = config_class

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
