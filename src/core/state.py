"""State representation for the Twerkflow workflow."""

from typing import Optional, Dict, Any
from pydantic import BaseModel, ConfigDict, Field


class TwerkflowState(BaseModel):
    """Represents the state of a workflow execution for a ticket."""

    # Allow nodes to add/manage custom keys dynamically
    model_config = ConfigDict(extra="allow")

    # Dynamic workflow state
    status: Optional[str] = None
    context: Dict[str, Any] = Field(default_factory=dict)
