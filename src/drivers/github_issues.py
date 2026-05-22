from src.drivers.base import TaskService
from typing import Dict, Any


class GitHubIssueTaskService(TaskService):
    def get_task(self, task_id: str) -> Dict[str, Any]:
        raise NotImplementedError("GitHubIssueTaskService.get_task not implemented")

    def update_task(self, task_id: str, data: Dict[str, Any]) -> None:
        raise NotImplementedError("GitHubIssueTaskService.update_task not implemented")
