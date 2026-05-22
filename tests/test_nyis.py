import pytest
from src.drivers.asana import AsanaTaskService
from src.drivers.github_pr import GitHubPRService
from src.drivers.github_wiki import GitHubWikiDocService
from src.drivers.notion import NotionDocService


def test_drivers_instantiation():
    # Test instantiation of NYI drivers
    with pytest.raises(NotImplementedError):
        AsanaTaskService().get_task("1")

    with pytest.raises(NotImplementedError):
        GitHubPRService().create_pr("b", "t", "d")

    with pytest.raises(NotImplementedError):
        GitHubWikiDocService().get_doc("1")

    with pytest.raises(NotImplementedError):
        NotionDocService().get_doc("1")
