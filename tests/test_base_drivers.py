"""Tests for base driver abstract classes."""

from src.drivers.base import DocService, PRService, TaskService


class DummyTask(TaskService):
    """Dummy implementation of TaskService for testing."""

    def get_task(self, id):
        """Mock get_task."""
        return {}

    def update_task(self, id, d):
        """Mock update_task."""
        pass

    def get_events(self, id):
        """Mock get_events."""
        return []

    def get_comments(self, id):
        """Mock get_comments."""
        return []

    def update_twerkflow_state(self, id, state):
        """Mock update_twerkflow_state."""
        pass

    def list_issues_by_label(self, label):
        """Mock list_issues_by_label."""
        return []


class DummyDoc(DocService):
    """Dummy implementation of DocService for testing."""

    def get_doc(self, id):
        """Mock get_doc."""
        return ""

    def write_doc(self, id, c, t=None):
        """Mock write_doc."""
        pass


class DummyPR(PRService):
    """Dummy implementation of PRService for testing."""

    def create_pr(self, b, t, d):
        """Mock create_pr."""
        return "pr"


def test_base_drivers():
    """Verifies that dummy driver implementations work."""
    task = DummyTask()
    task.update_task("1", {})
    task.update_twerkflow_state("1", {})
    assert task.get_task("1") == {}
    assert task.get_events("1") == []
    assert task.get_comments("1") == []
    assert task.list_issues_by_label("test") == []
