from src.drivers.base import DocService
from typing import Optional


class GitHubWikiDocService(DocService):
    def get_doc(self, doc_id: str) -> str:
        raise NotImplementedError("GitHubWikiDocService.get_doc not implemented")

    def write_doc(self, doc_id: str, content: str, title: Optional[str] = None) -> None:
        raise NotImplementedError("GitHubWikiDocService.write_doc not implemented")
