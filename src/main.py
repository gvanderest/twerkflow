from src.workflows.naive_flow import app
from src.core.state import TwerkflowState


def run_twerkflow(ticket_id: str, tags: list):
    initial_state = TwerkflowState(
        ticket_id=ticket_id,
        ticket_title="Example Ticket",
        tags=tags,
        status="pending",
        messages=[]
    )

    result = app.invoke(initial_state)
    print(f"Final state: {result}")


if __name__ == "__main__":
    # Test 1: Tagged (Should process)
    print("--- Test 1: Tagged ---")
    run_twerkflow("123", ["twerkflow", "design"])

    # Test 2: Untagged (Should abort)
    print("\n--- Test 2: Untagged ---")
    run_twerkflow("456", ["something-else"])
