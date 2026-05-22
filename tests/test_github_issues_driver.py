"""Tests for GitHub issues driver."""

from unittest.mock import MagicMock
from src.drivers.github_issues import GitHubIssueTaskService


def test_github_issue_driver_methods():
    """Verifies all GitHubIssueTaskService methods."""
    mock_repo = MagicMock()

    # Mock issue
    mock_issue = MagicMock()
    mock_issue.number = 123
    mock_issue.title = "Test"
    mock_issue.body = (
        "Body\n\n```\n<twerkflow>\n<state>\n"
        '{"ticket_id":"123","status":"pending"}\n'
        "</state>\n</twerkflow>\n```"
    )
    mock_issue.state = "open"
    mock_issue.labels = [MagicMock(name="tag1")]
    mock_repo.get_issue.return_value = mock_issue

    # Mock events/comments
    mock_event = MagicMock()
    mock_event.event = "labeled"
    mock_event.actor = MagicMock(login="user")
    mock_event.created_at = "2023-01-01"
    mock_issue.get_events.return_value = [mock_event]

    mock_comment = MagicMock()
    mock_comment.user = MagicMock(login="user")
    mock_comment.body = "comment"
    mock_comment.created_at = "2023-01-01"
    mock_issue.get_comments.return_value = [mock_comment]

    driver = GitHubIssueTaskService(repo=mock_repo)

    assert driver.get_task("123")["title"] == "Test"
    assert driver.get_events("123")[0]["event"] == "labeled"
    assert driver.get_comments("123")[0]["body"] == "comment"
    assert driver.list_issues_by_label("twerkflow") == []

    driver.update_task("123", {"status": "closed", "labels": ["tag2"]})
    mock_issue.edit.assert_called_with(state="closed")
    mock_issue.set_labels.assert_called_with("tag2")

    # Test state persistence
    state = driver.get_twerkflow_state("123")
    assert state is not None
    assert state.ticket_id == "123"

    state.status = "done"
    driver.update_twerkflow_state("123", state)

    # Check if issue edit was called with the updated state in body
    args, kwargs = mock_issue.edit.call_args
    assert "body" in kwargs
    assert "done" in kwargs["body"]
    assert "```\n<twerkflow>\n<state>" in kwargs["body"]
