from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List


class TaskService(ABC):
    @abstractmethod
    def get_task(self, task_id: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def update_task(self, task_id: str, data: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    def get_events(self, task_id: str) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_comments(self, task_id: str) -> List[Dict[str, Any]]:
        pass


class DocService(ABC):
    @abstractmethod
    def get_doc(self, doc_id: str) -> str:
        pass

    @abstractmethod
    def write_doc(self, doc_id: str, content: str, title: Optional[str] = None) -> None:
        pass


class PRService(ABC):
    @abstractmethod
    def create_pr(self, branch: str, title: str, description: str) -> str:
        pass
