"""State representation for the Twerkflow workflow."""

from typing import Optional
from pydantic import BaseModel, ConfigDict


class TwerkflowState(BaseModel):
    """Represents the state of a workflow execution for a ticket."""

    # Allow nodes to add/manage custom keys dynamically
    model_config = ConfigDict(extra="allow")

    status: Optional[str] = None

    # Store any dynamic state in __pydantic_extra__
    # This allows nodes to set state.my_key = "value"
