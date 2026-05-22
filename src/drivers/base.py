"""Defines base abstract classes for task, document, and PR services."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class TaskService(ABC):
    """Abstract base class for task services."""

    @abstractmethod
    def get_task(self, task_id: str) -> Dict[str, Any]:
        """Fetches a task."""
        pass

    @abstractmethod
    def update_task(self, task_id: str, data: Dict[str, Any]) -> None:
        """Updates a task."""
        pass

    @abstractmethod
    def get_events(self, task_id: str) -> List[Dict[str, Any]]:
        """Fetches events for a task."""
        pass

    @abstractmethod
    def get_comments(self, task_id: str) -> List[Dict[str, Any]]:
        """Fetches comments for a task."""
        pass

    @abstractmethod
    def list_issues_by_label(self, label: str) -> List[Dict[str, Any]]:
        """Lists issues with a specific label."""
        pass


class DocService(ABC):
    """Abstract base class for document services."""

    @abstractmethod
    def get_doc(self, doc_id: str) -> str:
        """Fetches a document."""
        pass

    @abstractmethod
    def write_doc(self, doc_id: str, content: str, title: Optional[str] = None) -> None:
        """Writes a document."""
        pass


class PRService(ABC):
    """Abstract base class for Pull Request services."""

    @abstractmethod
    def create_pr(self, branch: str, title: str, description: str) -> str:
        """Creates a Pull Request."""
        pass
