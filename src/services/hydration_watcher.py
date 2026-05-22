"""Provides a watcher service for hydration workflow."""

import time
from typing import Any, Callable, Optional
from pydantic import BaseModel, ConfigDict
from src.core.state import TwerkflowState
from src.core.config_loader import load_settings


class HydrationWatcherConfig(BaseModel):
    """Configuration for HydrationWatcher."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    factory: Any
    app: Any
    sleep_func: Callable[[float], None] = time.sleep
    load_settings_func: Callable[[], Any] = load_settings


class HydrationWatcher:
    """Watcher service for hydration."""

    def __init__(self, config: HydrationWatcherConfig):
        """Initializes the HydrationWatcher."""
        self.factory = config.factory
        self.app = config.app
        self.sleep_func = config.sleep_func
        self.settings = config.load_settings_func()

    def run_once(self, ticket_id: Optional[str], tags: list):
        """Executes the workflow once for a given ticket."""
        task_service = self.factory.get_task_service()
        config = {"configurable": {"task_service": task_service, "tags": tags}}

        # Hydration flow doesn't need ticket_id initially
        initial_state = TwerkflowState(status="pending")

        result = self.app.invoke(initial_state, config=config)
        print(f"Hydration Cycle Result: {result}")
        return result

    def run_watcher(self, iterations: int = 0):
        """Runs the hydration watcher service loop."""
        interval = self.settings.poll_interval_seconds
        count = 0
        while iterations == 0 or count < iterations:
            self.run_once(None, ["twerkflow"])

            # Add delay between hydration loop iterations
            if iterations == 0 or count < iterations - 1:
                print(f"--- Cycle complete, sleeping for {interval}s ---")
                self.sleep_func(interval)

            count += 1
