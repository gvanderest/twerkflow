"""Tests for main workflow entry point."""

from unittest.mock import MagicMock
from src.main import run_twerkflow
from src.core.driver_factory import DriverFactory


def test_run_twerkflow():
    """Verifies workflow execution."""
    # Setup mocks
    mock_app = MagicMock()
    mock_factory = MagicMock(spec=DriverFactory)
    mock_task_service = MagicMock()
    mock_factory.get_task_service.return_value = mock_task_service

    # Mock app invocation result
    mock_app.invoke.return_value = {"status": "completed"}

    # Execute
    result = run_twerkflow("123", ["tag"], mock_app, mock_factory)

    # Assertions
    assert result == {"status": "completed"}
    mock_app.invoke.assert_called_once()
    assert mock_app.invoke.call_args[0][0].ticket_id == "123"
    assert mock_app.invoke.call_args[1]["config"]["configurable"]["task_service"] == mock_task_service
