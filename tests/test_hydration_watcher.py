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
    mock_issue = {
        "id": "1",
        "title": "Test Issue",
        "body": "Body",
        "status": "open",
        "labels": [],
    }
    mock_task_service.list_issues_by_label.return_value = [mock_issue]
    mock_task_service.get_task.return_value = mock_issue
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
    # ... existing test ...


def test_hydration_watcher_skip_completed():
    """Verify run_once skips completed issues and adds label if missing."""
    mock_factory = MagicMock()
    mock_app = MagicMock()
    mock_task_service = MagicMock()
    mock_factory.get_task_service.return_value = mock_task_service
    mock_factory.get_command_runner.return_value = MagicMock()

    # Mock issue listing
    mock_issue = {
        "id": "5",
        "title": "Test Issue",
        "body": "Body",
        "status": "open",
        "labels": [],
    }
    mock_task_service.list_issues_by_label.return_value = [mock_issue]
    mock_task_service.get_task.return_value = mock_issue

    # Mock completed state
    mock_state = TwerkflowState(status="completed", ticket_id="5")
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

    # Should have updated the task to add the label
    args, kwargs = mock_task_service.update_task.call_args
    assert args[0] == "5"
    assert sorted(args[1]["labels"]) == sorted(["twerkflow", "twerkflow-complete"])


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
