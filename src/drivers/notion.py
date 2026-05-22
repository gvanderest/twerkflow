from src.drivers.base import DocService
from typing import Optional


class NotionDocService(DocService):
    def get_doc(self, doc_id: str) -> str:
        raise NotImplementedError("NotionDocService.get_doc not implemented")

    def write_doc(self, doc_id: str, content: str, title: Optional[str] = None) -> None:
        raise NotImplementedError("NotionDocService.write_doc not implemented")
