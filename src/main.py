"""Main entry point for the Twerkflow."""

from typing import Any, Optional

from src.core.driver_factory import DriverFactory
from src.core.state import TwerkflowState


def run_twerkflow(ticket_id: Optional[str], tags: list, app: Any, factory: DriverFactory):
    """Executes the Twerkflow workflow for a given ticket."""
    task_service = factory.get_task_service()

    config = {"configurable": {"task_service": task_service}}

    initial_state = TwerkflowState(
        ticket_id=ticket_id,
        ticket_title="Example Ticket",
        tags=tags,
        status="pending",
        messages=[],
    )

    result = app.invoke(initial_state, config=config)
    print(f"Final state: {result}")
    return result


if __name__ == "__main__":
    from src.workflows.hydration_flow import app

    # Test: Run hydration (should find tagged issues)
    print("--- Test: Hydration Flow ---")

    # Passing None for ticket_id as hydration flow discovers them
    factory = DriverFactory()
    run_twerkflow(None, ["twerkflow"], app, factory)
