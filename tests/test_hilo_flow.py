"""Tests for hilo flow."""

from unittest.mock import MagicMock
from src.core.state import TwerkflowState
from src.workflows.hilo_flow import abort_task, finalize_task, process_task, polling_node


def test_hilo_nodes():
    """Verify individual node logic for HILO flow."""
    state = TwerkflowState(status="pending", messages=[])
    config = {"configurable": {"ticket_id": "123"}}

    # Test finalize_task
    new_state = finalize_task(state, config)
    assert new_state.status == "done"
    assert "Task finalized" in new_state.messages

    # Test abort_task
    state.status = "pending"
    new_state = abort_task(state, config)
    assert new_state.status == "aborted"
    assert "Abort triggered" in new_state.messages

    # Test process_task
    state.status = "pending"
    new_state = process_task(state, config)
    assert new_state.status == "processing"
    assert "Started processing" in new_state.messages

    # Test polling_node (already approved)
    mock_task_service = MagicMock()
    mock_task_service.get_comments.return_value = [{"body": "twerkflow approve 123"}]
    mock_settings = MagicMock()
    mock_settings.poll_interval_seconds = 0
    config_poll = {
        "configurable": {
            "ticket_id": "123",
            "task_service": mock_task_service,
            "settings": mock_settings,
            "sleep_func": MagicMock(),
        }
    }
    state.status = "pending"
    new_state = polling_node(state, config_poll)
    assert new_state.status == "approved"
