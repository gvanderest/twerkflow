"""Provides a service to interact with GitHub wiki."""

from typing import Optional

from src.drivers.base import DocService


class GitHubWikiDocService(DocService):
    """Service to interact with GitHub wiki."""

    def get_doc(self, doc_id: str) -> str:
        """Fetches a document from GitHub wiki."""
        raise NotImplementedError("GitHubWikiDocService.get_doc not implemented")

    def write_doc(self, doc_id: str, content: str, title: Optional[str] = None) -> None:
        """Writes a document to GitHub wiki."""
        raise NotImplementedError("GitHubWikiDocService.write_doc not implemented")
