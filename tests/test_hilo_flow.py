"""Tests for hilo flow."""

import pytest
from unittest.mock import MagicMock
from src.core.state import TwerkflowState
from src.workflows.hilo_flow import (
    abort_task,
    finalize_task,
    process_task,
    polling_node,
    gate_check_tag,
    check_approval,
    check_polling_status,
)


def test_hilo_nodes():
    """Verify individual node logic for HILO flow."""
    state = TwerkflowState()
    config = {"configurable": {"ticket_id": "123"}}

    # Test finalize_task
    state = TwerkflowState(status="pending", messages=[])
    new_state = finalize_task(state, config)
    assert new_state.status == "done"
    assert new_state.messages == ["Task finalized"]

    # Test abort_task
    state = TwerkflowState(status="pending", messages=[])
    new_state = abort_task(state, config)
    assert new_state.status == "aborted"
    assert new_state.messages == ["Abort triggered"]

    # Test process_task
    state = TwerkflowState(status="pending", messages=[])
    new_state = process_task(state, config)
    assert new_state.status == "processing"
    assert new_state.messages == ["Started processing"]

    # Test process_task error
    with pytest.raises(ValueError, match="Cannot process task without ticket_id"):
        process_task(state, {"configurable": {}})


def test_hilo_flow_gate_check_tag():
    """Verify gate_check_tag logic."""
    state = TwerkflowState()

    # Test tagged
    config_tagged = {"configurable": {"tags": ["twerkflow"]}}
    assert gate_check_tag(state, config_tagged) == "process"

    # Test untagged
    config_untagged = {"configurable": {"tags": ["other"]}}
    assert gate_check_tag(state, config_untagged) == "abort"


def test_hilo_flow_polling_logic():
    """Verify polling node and approval logic."""
    mock_task_service = MagicMock()
    mock_settings = MagicMock()
    mock_settings.poll_interval_seconds = 0

    # Setup test with no approval
    mock_task_service.get_comments.return_value = [{"body": "no approval"}]
    config = {
        "configurable": {
            "ticket_id": "123",
            "task_service": mock_task_service,
            "settings": mock_settings,
            "sleep_func": MagicMock(),
        }
    }

    state = TwerkflowState(status="pending", messages=[])

    # Check approval
    assert check_approval(state, config) == "pending"

    # Polling node should keep status pending
    new_state = polling_node(state, config)
    assert new_state.status == "pending"

    # Now mock approval
    mock_task_service.get_comments.return_value = [{"body": "twerkflow approve 123"}]
    new_state = polling_node(state, config)
    assert new_state.status == "approved"

    # Check polling status conditional
    assert check_polling_status(new_state) == "approved"
    state.status = "pending"
    assert check_polling_status(state) == "pending"

    # Test polling_node error
    with pytest.raises(ValueError, match="Cannot poll without ticket_id"):
        polling_node(state, {"configurable": {}})

    # Test check_approval error
    assert check_approval(state, {"configurable": {}}) == "pending"
