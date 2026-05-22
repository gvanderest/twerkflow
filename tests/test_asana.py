"""Tests for Asana driver."""

import pytest
from src.drivers.asana import AsanaTaskService


def test_asana_driver():
    """Verifies that AsanaTaskService methods raise NotImplementedError."""
    service = AsanaTaskService()
    with pytest.raises(NotImplementedError):
        service.get_task("1")
    with pytest.raises(NotImplementedError):
        service.update_task("1", {})
    with pytest.raises(NotImplementedError):
        service.get_events("1")
    with pytest.raises(NotImplementedError):
        service.get_comments("1")
