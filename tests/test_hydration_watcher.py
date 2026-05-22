"""Tests for hydration watcher service."""

from unittest.mock import MagicMock
from src.services.hydration_watcher import HydrationWatcher, HydrationWatcherConfig


def test_hydration_watcher_run_once():
    """Verify run_once executes one hydration cycle."""
    mock_factory = MagicMock()
    mock_app = MagicMock()
    mock_task_service = MagicMock()
    mock_factory.get_task_service.return_value = mock_task_service

    # Mock invoke result
    mock_app.invoke.return_value = {"status": "hydrated"}

    # Mock issue listing
    mock_task_service.list_issues_by_label.return_value = [
        {"id": "1", "title": "Test Issue", "body": "Body", "status": "open"}
    ]

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
    result = watcher.run_once(None, ["twerkflow"])

    assert result is None  # run_once returns None, the loop processes issues
    # But wait, run_once now iterates, so we should check if app.invoke was called
    mock_app.invoke.assert_called_once()
    assert mock_factory.get_task_service.called


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
