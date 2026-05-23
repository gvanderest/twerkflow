"""Tests for hydration watcher service."""

from unittest.mock import MagicMock
from src.core.state import TwerkflowState
from src.services.hydration_watcher import HydrationWatcher, HydrationWatcherConfig


def test_hydration_watcher_run_once():
    """Verify run_once executes one hydration cycle."""
    mock_factory = MagicMock()
    mock_app = MagicMock()
    mock_task_service = MagicMock()
    mock_factory.get_task_service.return_value = mock_task_service
    mock_factory.get_command_runner.return_value = MagicMock()

    # Mock invoke result
    mock_app.invoke.return_value = TwerkflowState(status="completed", ticket_id="1")

    # Mock issue listing
    mock_task_service.list_issues_by_label.return_value = [
        {"id": "1", "title": "Test Issue", "body": "Body", "status": "open", "labels": []}
    ]
    # Mock existing state
    mock_task_service.get_twerkflow_state.return_value = None

    # Mock settings
    mock_settings = MagicMock()
    mock_settings.poll_interval_seconds = 0
    mock_load_settings = MagicMock(return_value=mock_settings)

    config = HydrationWatcherConfig(
        factory=mock_factory,
        app=mock_app,
        load_settings_func=mock_load_settings,
    )
    watcher = HydrationWatcher(config)
    watcher.run_once(None, ["twerkflow"])

    mock_app.invoke.assert_called_once()
    assert mock_factory.get_task_service.called


def test_hydration_watcher_resume():
    """Verify run_once resumes an existing workflow."""
    mock_factory = MagicMock()
    mock_app = MagicMock()
    mock_task_service = MagicMock()
    mock_factory.get_task_service.return_value = mock_task_service
    mock_factory.get_command_runner.return_value = MagicMock()

    # Mock issue listing
    mock_task_service.list_issues_by_label.return_value = [
        {"id": "1", "title": "Test Issue", "body": "Body", "status": "open", "labels": []}
    ]
    # Mock existing state
    mock_state = TwerkflowState(status="starting", ticket_id="1")
    mock_task_service.get_twerkflow_state.return_value = mock_state

    # Mock settings
    mock_settings = MagicMock()
    mock_settings.poll_interval_seconds = 0
    mock_load_settings = MagicMock(return_value=mock_settings)

    config = HydrationWatcherConfig(
        factory=mock_factory,
        app=mock_app,
        load_settings_func=mock_load_settings,
    )
    watcher = HydrationWatcher(config)
    watcher.run_once(None, ["twerkflow"])

    mock_app.invoke.assert_called_once()
    assert mock_app.invoke.call_args[0][0].status == "starting"


def test_hydration_watcher_run_watcher():
    """Verify run_watcher loops correctly."""
    mock_factory = MagicMock()
    mock_app = MagicMock()
    mock_sleep = MagicMock()

    # Mock settings
    mock_settings = MagicMock()
    mock_settings.poll_interval_seconds = 0
    mock_load_settings = MagicMock(return_value=mock_settings)

    config = HydrationWatcherConfig(
        factory=mock_factory,
        app=mock_app,
        sleep_func=mock_sleep,
        load_settings_func=mock_load_settings,
    )
    watcher = HydrationWatcher(config)

    watcher.run_watcher(iterations=2)

    assert mock_sleep.call_count == 1
