"""State representation for the Twerkflow workflow."""

from typing import List
from pydantic import BaseModel, Field


class TwerkflowState(BaseModel):
    """Represents the state of a workflow execution for a ticket."""

    ticket_id: str
    ticket_title: str
    tags: List[str] = Field(default_factory=list)
    status: str = "pending"
    messages: List[str] = Field(default_factory=list)
