"""Provides a service to interact with Asana tasks."""

from typing import Any, Dict, List

from src.drivers.base import TaskService


class AsanaTaskService(TaskService):
    """Service to interact with Asana tasks."""

    def get_task(self, task_id: str) -> Dict[str, Any]:
        """Fetches a task from Asana."""
        raise NotImplementedError("AsanaTaskService.get_task not implemented")

    def update_task(self, task_id: str, data: Dict[str, Any]) -> None:
        """Updates a task in Asana."""
        raise NotImplementedError("AsanaTaskService.update_task not implemented")

    def get_events(self, task_id: str) -> List[Dict[str, Any]]:
        """Fetches events for a task from Asana."""
        raise NotImplementedError("AsanaTaskService.get_events not implemented")

    def get_comments(self, task_id: str) -> List[Dict[str, Any]]:
        """Fetches comments for a task from Asana."""
        raise NotImplementedError("AsanaTaskService.get_comments not implemented")

    def list_issues_by_label(self, label: str) -> List[Dict[str, Any]]:
        """Lists issues with a specific label from Asana."""
        raise NotImplementedError("AsanaTaskService.list_issues_by_label not implemented")
