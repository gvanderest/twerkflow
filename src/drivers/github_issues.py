"""Provides a service to interact with GitHub issues."""

import re
from typing import Any, Dict, List, Optional

from src.drivers.base import TaskService
from src.core.state import TwerkflowState


class GitHubIssueTaskService(TaskService):
    """Service to interact with GitHub issues."""

    def __init__(self, repo: Any):
        """Initializes the GitHubIssueTaskService."""
        self.repo = repo
        self._state_pattern = re.compile(r"<twerkflow-state>(.*?)</twerkflow-state>", re.DOTALL)

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

    def get_twerkflow_state(self, task_id: str) -> Optional[TwerkflowState]:
        """Fetches and parses the twerkflow state from an issue."""
        issue = self.repo.get_issue(int(task_id))
        match = self._state_pattern.search(issue.body)
        if not match:
            return None

        state_json = match.group(1)
        return TwerkflowState.model_validate_json(state_json)

    def update_twerkflow_state(self, task_id: str, state: TwerkflowState) -> None:
        """Updates the twerkflow state in an issue."""
        issue = self.repo.get_issue(int(task_id))
        state_json = state.model_dump_json(indent=2)
        new_state_block = f"<twerkflow-state>\n{state_json}\n</twerkflow-state>"

        # Replace or append
        if self._state_pattern.search(issue.body):
            new_body = self._state_pattern.sub(new_state_block, issue.body)
        else:
            new_body = f"{issue.body}\n\n{new_state_block}"

        issue.edit(body=new_body)

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
