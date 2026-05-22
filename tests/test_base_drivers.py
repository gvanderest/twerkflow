from src.drivers.base import TaskService, DocService, PRService


class DummyTask(TaskService):
    def get_task(self, id):
        return {}

    def update_task(self, id, d):
        pass

    def get_events(self, id):
        return []

    def get_comments(self, id):
        return []


class DummyDoc(DocService):
    def get_doc(self, id):
        return ""

    def write_doc(self, id, c, t=None):
        pass


class DummyPR(PRService):
    def create_pr(self, b, t, d):
        return "pr"


def test_base_drivers():
    task = DummyTask()
    task.update_task("1", {})
    assert task.get_task("1") == {}
    assert task.get_events("1") == []
    assert task.get_comments("1") == []

    doc = DummyDoc()
    doc.write_doc("1", "content")
    assert doc.get_doc("1") == ""

    assert DummyPR().create_pr("b", "t", "d") == "pr"
