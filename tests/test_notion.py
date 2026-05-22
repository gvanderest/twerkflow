"""Tests for Notion driver."""

import pytest
from src.drivers.notion import NotionDocService


def test_notion_driver():
    """Verifies that NotionDocService methods raise NotImplementedError."""
    service = NotionDocService()
    with pytest.raises(NotImplementedError):
        service.get_doc("1")
    with pytest.raises(NotImplementedError):
        service.write_doc("1", "content", title="title")
