from typing import Any
from src.core.state import TwerkflowState
from src.core.driver_factory import DriverFactory


def run_twerkflow(
    ticket_id: str,
    tags: list,
    app: Any,
    factory: DriverFactory
):
    task_service = factory.get_task_service()

    config = {"configurable": {"task_service": task_service}}

    initial_state = TwerkflowState(
        ticket_id=ticket_id,
        ticket_title="Example Ticket",
        tags=tags,
        status="pending",
        messages=[]
    )

    result = app.invoke(initial_state, config=config)
    print(f"Final state: {result}")
    return result


if __name__ == "__main__":
    from src.workflows.naive_flow import app
    # Test 1: Tagged (Should process)
    print("--- Test 1: Tagged ---")
    run_twerkflow("123", ["twerkflow", "design"], app, DriverFactory())

    # Test 2: Untagged (Should abort)
    print("\n--- Test 2: Untagged ---")
    run_twerkflow("456", ["something-else"], app, DriverFactory())
