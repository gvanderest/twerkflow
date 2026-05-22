"""State representation for the Twerkflow workflow."""

from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field


class TwerkflowState(BaseModel):
    """Represents the state of a workflow execution for a ticket."""

    # Allow nodes to add/manage custom keys dynamically
    model_config = ConfigDict(extra="allow")

    status: Optional[str] = None
    messages: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)

    # Store any dynamic state in __pydantic_extra__
    # This allows nodes to set state.my_key = "value"
