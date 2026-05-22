from typing import List
from pydantic import BaseModel, Field


class TwerkflowState(BaseModel):
    ticket_id: str
    ticket_title: str
    tags: List[str] = Field(default_factory=list)
    status: str = "pending"
    messages: List[str] = Field(default_factory=list)
