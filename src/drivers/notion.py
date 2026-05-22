"""Provides a service to interact with Notion documents."""

from typing import Optional

from src.drivers.base import DocService


class NotionDocService(DocService):
    """Service to interact with Notion documents."""

    def __init__(self, token: Optional[str] = None):
        """Initializes the NotionDocService."""
        self.token = token

    def get_doc(self, doc_id: str) -> str:
        """Fetches a document from Notion."""
        raise NotImplementedError("NotionDocService.get_doc not implemented")

    def write_doc(self, doc_id: str, content: str, title: Optional[str] = None) -> None:
        """Writes a document to Notion."""
        raise NotImplementedError("NotionDocService.write_doc not implemented")
