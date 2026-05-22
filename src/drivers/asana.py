from src.drivers.base import TaskService
from typing import Dict, Any, List


class AsanaTaskService(TaskService):
    def get_task(self, task_id: str) -> Dict[str, Any]:
        raise NotImplementedError("AsanaTaskService.get_task not implemented")

    def update_task(self, task_id: str, data: Dict[str, Any]) -> None:
        raise NotImplementedError("AsanaTaskService.update_task not implemented")

    def get_events(self, task_id: str) -> List[Dict[str, Any]]:
        raise NotImplementedError("AsanaTaskService.get_events not implemented")

    def get_comments(self, task_id: str) -> List[Dict[str, Any]]:
        raise NotImplementedError("AsanaTaskService.get_comments not implemented")
