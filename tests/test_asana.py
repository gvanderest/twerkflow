import pytest
from src.drivers.asana import AsanaTaskService
from src.drivers.base import TaskService

def test_asana_driver():
    service = AsanaTaskService()
    with pytest.raises(NotImplementedError):
        service.get_task("1")
    with pytest.raises(NotImplementedError):
        service.update_task("1", {})
    with pytest.raises(NotImplementedError):
        service.get_events("1")
    with pytest.raises(NotImplementedError):
        service.get_comments("1")
