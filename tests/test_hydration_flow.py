"""Tests for hydration workflow."""

from unittest.mock import MagicMock
from src.core.state import TwerkflowState
from src.workflows.hydration_flow import app, check_hydration_status, delay_node


def test_hydration_flow_success():
    """Verify hydration flow lists issues and finishes."""
    mock_task_service = MagicMock()
    mock_settings = MagicMock()
    mock_settings.get_driver_config.return_value.params.get.return_value = "twerkflow"

    # Mock issue listing
    mock_task_service.list_issues_by_label.return_value = [
        {"id": "1", "title": "Test Issue", "body": "Body", "status": "open"}
    ]

    config = {
        "configurable": {
            "task_service": mock_task_service,
            "settings": mock_settings,
            "command_runner": MagicMock(),
            "ticket_id": "1",
        }
    }

    state = TwerkflowState(
        status="pending",
    )

    result = app.invoke(state, config=config)

    assert result["status"] == "completed"
    mock_task_service.list_issues_by_label.assert_called_once()
    # Check persistence call
    assert mock_task_service.update_twerkflow_state.called


def test_nodes_and_edges():
    """Test individual nodes and conditional edges."""
    state = TwerkflowState(ticket_id="0", status="pending")

    # Test delay_node
    mock_sleep = MagicMock()
    mock_settings = MagicMock()
    mock_settings.poll_interval_seconds = 0
    config = {"configurable": {"settings": mock_settings, "sleep_func": mock_sleep}}

    new_state = delay_node(state, config)
    assert new_state.status == "pending"
    assert mock_sleep.called

    # Test check_hydration_status
    state.status = "starting"
    assert check_hydration_status(state) == "finished"
    state.status = "pending"
    assert check_hydration_status(state) == "delay"
