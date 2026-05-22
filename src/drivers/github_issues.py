from src.drivers.base import TaskService
from typing import Dict, Any, List
import os
from github import Github


class GitHubIssueTaskService(TaskService):
    def __init__(self, repo_name: str):
        self.github = Github(os.getenv("GITHUB_TOKEN"))
        self.repo = self.github.get_repo(repo_name)

    def get_task(self, task_id: str) -> Dict[str, Any]:
        issue = self.repo.get_issue(int(task_id))
        return {
            "id": str(issue.number),
            "title": issue.title,
            "body": issue.body,
            "status": issue.state,
            "tags": [label.name for label in issue.labels]
        }

    def update_task(self, task_id: str, data: Dict[str, Any]) -> None:
        issue = self.repo.get_issue(int(task_id))
        if "status" in data:
            issue.edit(state=data["status"])
        if "labels" in data:
            issue.set_labels(*data["labels"])

    def get_events(self, task_id: str) -> List[Dict[str, Any]]:
        issue = self.repo.get_issue(int(task_id))
        # Note: PyGithub events are complex objects, simplify to dict
        return [
            {"event": e.event, "actor": e.actor.login, "created_at": str(e.created_at)}
            for e in issue.get_events()
        ]

    def get_comments(self, task_id: str) -> List[Dict[str, Any]]:
        issue = self.repo.get_issue(int(task_id))
        return [
            {"user": c.user.login, "body": c.body, "created_at": str(c.created_at)}
            for c in issue.get_comments()
        ]
