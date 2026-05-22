"""Tests for hydration workflow."""

from unittest.mock import MagicMock
from src.core.state import TwerkflowState
from src.workflows.hydration_flow import app


def test_hydration_flow():
    """Verify hydration flow lists issues."""
    mock_task_service = MagicMock()

    # Mock issue listing
    mock_task_service.list_issues_by_label.return_value = [
        {"id": "1", "title": "Test Issue", "body": "Body", "status": "open"}
    ]

    config = {"configurable": {"task_service": mock_task_service}}

    state = TwerkflowState(
        ticket_id="0",
        ticket_title="Root",
        tags=["twerkflow"],
        status="pending",
        messages=[],
    )

    result = app.invoke(state, config=config)

    assert result["status"] == "hydrated"
    mock_task_service.list_issues_by_label.assert_called_once()
