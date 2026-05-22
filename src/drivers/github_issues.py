"""Provides a service to interact with GitHub issues."""

from typing import Any, Dict, List

from src.drivers.base import TaskService


class GitHubIssueTaskService(TaskService):
    """Service to interact with GitHub issues."""

    def __init__(self, repo: Any):
        """Initializes the GitHubIssueTaskService."""
        self.repo = repo

    def get_task(self, task_id: str) -> Dict[str, Any]:
        """Fetches a task from GitHub issues."""
        issue = self.repo.get_issue(int(task_id))
        return {
            "id": str(issue.number),
            "title": issue.title,
            "body": issue.body,
            "status": issue.state,
            "tags": [label.name for label in issue.labels],
        }

    def update_task(self, task_id: str, data: Dict[str, Any]) -> None:
        """Updates a task in GitHub issues."""
        issue = self.repo.get_issue(int(task_id))
        if "status" in data:
            issue.edit(state=data["status"])
        if "labels" in data:
            issue.set_labels(*data["labels"])

    def get_events(self, task_id: str) -> List[Dict[str, Any]]:
        """Fetches events for a task from GitHub issues."""
        issue = self.repo.get_issue(int(task_id))
        # Note: PyGithub events are complex objects, simplify to dict
        return [
            {
                "event": e.event,
                "actor": e.actor.login if e.actor else "unknown",
                "created_at": str(e.created_at),
            }
            for e in issue.get_events()
        ]

    def get_comments(self, task_id: str) -> List[Dict[str, Any]]:
        """Fetches comments for a task from GitHub issues."""
        issue = self.repo.get_issue(int(task_id))
        return [{"user": c.user.login, "body": c.body, "created_at": str(c.created_at)} for c in issue.get_comments()]
