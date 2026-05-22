"""Tests for experiment flow."""

from unittest.mock import MagicMock
from src.core.state import TwerkflowState
from src.workflows.experiment_flow import generate_fortune, start_node, check_status


def test_generate_fortune():
    """Verify generate_fortune generates fortune and comments."""
    mock_runner = MagicMock()
    mock_runner.run.return_value = "Fortune favors the bold."
    mock_task_service = MagicMock()

    config = {
        "configurable": {
            "ticket_id": "1",
            "command_runner": mock_runner,
            "task_service": mock_task_service,
        }
    }

    state = TwerkflowState(status="starting", ticket_id="1")

    result = generate_fortune(state, config)

    assert result.status == "completed"
    assert mock_runner.run.call_count == 2
    assert mock_task_service.update_twerkflow_state.called


def test_nodes():
    """Verify nodes."""
    state = TwerkflowState(status="pending")
    new_state = start_node(state, {})
    assert new_state.status == "starting"

    state.status = "completed"
    assert check_status(state) == "end"
    state.status = "starting"
    assert check_status(state) == "process"
