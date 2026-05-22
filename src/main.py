"""Main entry point for the Twerkflow."""

import time
import argparse
from typing import Any, Optional
from src.core.driver_factory import DriverFactory
from src.core.state import TwerkflowState
from src.core.config_loader import load_settings
from src.workflows.hydration_flow import app


def run_twerkflow(ticket_id: Optional[str], tags: list, app: Any, factory: DriverFactory):
    """Executes the Twerkflow workflow for a given ticket."""
    task_service = factory.get_task_service()

    config = {
        "configurable": {
            "task_service": task_service,
            "ticket_id": ticket_id,
            "tags": tags,
        }
    }

    initial_state = TwerkflowState(
        status="pending",
        messages=[],
    )

    result = app.invoke(initial_state, config=config)
    print(f"Final state: {result}")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Twerkflow Hydration Watcher")
    parser.add_argument("--iterations", type=int, default=0, help="Number of iterations to run (0 for infinite)")
    args = parser.parse_args()

    # Test: Run hydration (should find tagged issues)
    print(f"--- Starting Hydration Watcher (iterations: {args.iterations or 'infinite'}) ---")

    factory = DriverFactory()
    settings = load_settings()
    interval = settings.poll_interval_seconds

    count = 0
    while args.iterations == 0 or count < args.iterations:
        run_twerkflow(None, ["twerkflow"], app, factory)

        # Add delay between hydration loop iterations
        print(f"--- Cycle complete, sleeping for {interval}s ---")
        time.sleep(interval)

        count += 1
