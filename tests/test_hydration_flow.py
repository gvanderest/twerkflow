"""Tests for hydration workflow."""

from unittest.mock import MagicMock
from src.core.state import TwerkflowState
from src.core.types import WorkflowConfig
from src.workflows.hydration_flow import app, check_hydration_status, delay_node
from src.drivers.base import TaskService
from src.services.command_runner import CommandRunner

def test_hydration_flow_success():
    """Verify hydration flow persists state and finishes."""
    mock_task_service = MagicMock(spec=TaskService)

    config = {
        "configurable": WorkflowConfig(
            task_service=mock_task_service,
            ticket_id="1",
            command_runner=MagicMock(spec=CommandRunner),
            tags=["twerkflow"],
        )
    }

    state = TwerkflowState(
        status="pending",
        ticket_id="1",
    )

    result = app.invoke(state, config=config)  # type: ignore

    assert result["status"] == "completed"
    # Check persistence call
    assert mock_task_service.update_twerkflow_state.called


def test_nodes_and_edges():
    """Test individual nodes and conditional edges."""
    state = TwerkflowState(status="pending", ticket_id="1")

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
    state.status = "completed"
    assert check_hydration_status(state) == "finished"
    state.status = "pending"
    assert check_hydration_status(state) == "delay"
