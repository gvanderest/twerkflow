"""Tests for HILO workflow."""

import os
from unittest.mock import MagicMock
from src.core.state import TwerkflowState
from src.workflows.hilo_flow import app

# Set dummy token for testing
os.environ["GITHUB_TOKEN"] = "dummy"


class MockSettings:
    """Mock settings for testing."""

    def __init__(self, interval):
        self.poll_interval_seconds = interval


def test_hilo_flow_abort():
    """Verify abort behavior."""
    mock_task_service = MagicMock()
    config = {
        "configurable": {
            "task_service": mock_task_service,
            "ticket_id": "123",
            "tags": ["other"],
        }
    }

    state = TwerkflowState(status="pending", messages=[])

    result = app.invoke(state, config=config)
    # result is a dict, need to get the final state
    assert result["status"] == "aborted"
    assert "Abort triggered" in result["messages"]


def test_hilo_flow_approval():
    """Verify approval behavior."""
    mock_task_service = MagicMock()

    # Mock comments to include approval
    mock_task_service.get_comments.return_value = [
        {"user": "user", "body": "twerkflow approve design", "created_at": "2023-01-01"}
    ]

    mock_sleep = MagicMock()
    mock_settings = MockSettings(interval=0)

    config = {
        "configurable": {
            "task_service": mock_task_service,
            "sleep_func": mock_sleep,
            "settings": mock_settings,
            "ticket_id": "123",
            "tags": ["twerkflow"],
        }
    }

    state = TwerkflowState(
        status="pending",
        messages=[],
    )

    result = app.invoke(state, config=config)
    assert result["status"] == "done"
    assert "Task finalized" in result["messages"]
