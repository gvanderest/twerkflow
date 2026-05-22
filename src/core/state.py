"""State representation for the Twerkflow workflow."""

from typing import List, Optional
from pydantic import BaseModel, Field


class TwerkflowState(BaseModel):
    """Represents the state of a workflow execution for a ticket."""

    ticket_id: Optional[str] = None
    ticket_title: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    status: str = "pending"
    messages: List[str] = Field(default_factory=list)
