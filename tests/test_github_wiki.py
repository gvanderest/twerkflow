import pytest
from src.drivers.github_wiki import GitHubWikiDocService

def test_github_wiki_driver():
    service = GitHubWikiDocService()
    with pytest.raises(NotImplementedError):
        service.get_doc("1")
    with pytest.raises(NotImplementedError):
        service.write_doc("1", "content", title="title")
