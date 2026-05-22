"""Tests for Asana driver."""

import pytest
from unittest.mock import MagicMock
from src.drivers.asana import AsanaTaskService


def test_asana_task_service_raises():
    """Verifies that AsanaTaskService raises NotImplementedError for all methods."""
    service = AsanaTaskService()

    with pytest.raises(NotImplementedError):
        service.get_task("1")

    with pytest.raises(NotImplementedError):
        service.update_task("1", {})

    with pytest.raises(NotImplementedError):
        service.get_events("1")

    with pytest.raises(NotImplementedError):
        service.get_comments("1")

    with pytest.raises(NotImplementedError):
        service.list_issues_by_label("test")

    with pytest.raises(NotImplementedError):
        service.update_twerkflow_state("1", MagicMock())
