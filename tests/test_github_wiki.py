"""Tests for GitHub wiki driver."""

import pytest
from src.drivers.github_wiki import GitHubWikiDocService


def test_github_wiki_driver():
    """Verifies that GitHubWikiDocService methods raise NotImplementedError."""
    service = GitHubWikiDocService()
    with pytest.raises(NotImplementedError):
        service.get_doc("1")
    with pytest.raises(NotImplementedError):
        service.write_doc("1", "content", title="title")
