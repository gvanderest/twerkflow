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
        command_runner = self.factory.get_command_runner()

        # Discovery: find issues with twerkflow label
        issues = task_service.list_issues_by_label(tags[0])

        # Filter: ignore issues labeled 'complete' or 'hilo'
        candidates = [
            i
            for i in issues
            if not any(label.name in ["twerkflow-complete", "twerkflow-hilo"] for label in i.get("labels", []))
        ]

        # Find the first one that hasn't been hydrated (doesn't have twerkflow tag in body)
        # Note: assuming 'task_service.list_issues_by_label' returns objects with labels
        unhydrated_issues = [i for i in candidates if "<twerkflow>" not in i.get("body", "")]

        if not unhydrated_issues:
            # Check if there are any issues at all
            if candidates:
                print(f"--- All {len(candidates)} issues are already hydrated. ---")
            else:
                print("--- No issues found with tag 'twerkflow'. ---")
            return None

        issue = unhydrated_issues[0]
        print(f"--- Hydrating issue: {issue['id']} ---")

        config = {
            "configurable": {
                "task_service": task_service,
                "tags": tags,
                "ticket_id": issue["id"],
                "command_runner": command_runner,
            }
        }

        # State creation is now deferred until we have an ID
        initial_state = TwerkflowState(status="starting", ticket_id=issue["id"])

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
