"""Tests for naive workflow."""

from unittest.mock import MagicMock
from src.core.state import TwerkflowState
from src.workflows.naive_flow import app


def test_naive_flow_nodes():
    """Verifies naive workflow node logic."""
    state = TwerkflowState(status="pending", messages=[])
    config = {
        "configurable": {
            "task_service": MagicMock(),
            "ticket_id": "1",
            "tags": ["twerkflow"],
        }
    }

    result = app.invoke(state, config=config)
    assert result["status"] == "processing"


def test_naive_flow_abort():
    """Verifies naive workflow aborts correctly."""
    state = TwerkflowState(status="pending", messages=[])
    config = {
        "configurable": {
            "task_service": MagicMock(),
            "ticket_id": "1",
            "tags": ["other"],
        }
    }

    result = app.invoke(state, config=config)
    assert result["status"] == "aborted"
