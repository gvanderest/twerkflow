from unittest.mock import MagicMock
from src.workflows.naive_flow import gate_check_tag, process_task, abort_task
from src.core.state import TwerkflowState


def test_naive_flow_nodes():
    state = TwerkflowState(ticket_id="1", ticket_title="Test", tags=["twerkflow"])
    config = {"configurable": {"task_service": MagicMock()}}

    assert gate_check_tag(state, config) == "process"

    state.tags = []
    assert gate_check_tag(state, config) == "abort"

    # Test nodes
    process_task(state, config)
    assert state.status == "processing"

    abort_task(state, config)
    assert state.status == "aborted"
