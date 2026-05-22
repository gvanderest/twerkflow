"""Tests for main entry point."""

from unittest.mock import MagicMock
from src.main import run_watcher_app


def test_run_watcher_app():
    """Verify run_watcher_app initializes watcher."""
    mock_watcher_class = MagicMock()
    mock_watcher = MagicMock()
    mock_watcher_class.return_value = mock_watcher

    run_watcher_app(iterations=1, watcher_class=mock_watcher_class)

    mock_watcher.run_watcher.assert_called_once_with(iterations=1)
