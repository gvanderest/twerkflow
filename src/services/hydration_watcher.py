"""Provides a watcher service for hydration workflow."""

import time
from typing import Any, Callable, Dict, List, Optional
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

    def run_once(self, ticket_id: Optional[str], tags: List[str]) -> Optional[Dict[str, Any]]:
        """Executes the workflow once for a given ticket."""
        task_service = self.factory.get_task_service()
        command_runner = self.factory.get_command_runner()

        # Discovery: find issues with twerkflow label
        issues = task_service.list_issues_by_label(tags[0])

        # Filter: ignore issues labeled 'complete' or 'hilo'
        candidates = [
            i
            for i in issues
            if not any(label.get("name") in ["twerkflow-complete", "twerkflow-hilo"] for label in i.get("labels", []))
        ]

        if not candidates:
            print("--- No issues found with tag 'twerkflow'. ---")
            return None

        # Process candidates
        for issue in candidates:
            labels = [label.get("name") for label in issue.get("labels", [])]
            print(f"--- Processing issue: {issue['id']}, labels: {labels} ---")

            # Check if hydrated
            existing_state = task_service.get_twerkflow_state(issue["id"])

            if existing_state and existing_state.status == "completed":
                print(f"--- Issue {issue['id']} already completed, checking labels ---")
                labels = [label.get("name") for label in issue.get("labels", [])]
                if "twerkflow-complete" not in labels:
                    print(f"--- Issue {issue['id']} completed, adding label ---")
                    # Append new label, keep existing ones
                    new_labels = list(set(labels + [tags[0], "twerkflow-complete"]))
                    task_service.update_task(issue["id"], {"labels": new_labels})
                else:
                    print(f"--- Issue {issue['id']} already has 'twerkflow-complete' label, skipping ---")
                continue

            # Check if issue already has 'twerkflow-complete' (safety check)
            labels = [label.get("name") for label in issue.get("labels", [])]
            if "twerkflow-complete" in labels:
                print(f"--- Skipping issue {issue['id']} as it is already marked 'twerkflow-complete' ---")
                continue

            config = {
                "configurable": {
                    "task_service": task_service,
                    "tags": tags,
                    "ticket_id": issue["id"],
                    "command_runner": command_runner,
                }
            }

            if existing_state:
                print(f"--- Resuming issue: {issue['id']} (status: {existing_state.status}) ---")
                state = existing_state
            else:
                print(f"--- Hydrating issue: {issue['id']} ---")
                state = TwerkflowState(status="starting", ticket_id=issue["id"])

            # Execute workflow
            result = self.app.invoke(state, config=config)
            print(f"Cycle Result for {issue['id']}: {result}")

            # If completed, add label if missing
            status = getattr(result, "status", None)
            if not status and isinstance(result, dict):
                status = result.get("status")

            if status == "completed":
                labels = [label.get("name") for label in issue.get("labels", [])]
                if "twerkflow-complete" not in labels:
                    print(f"--- Issue {issue['id']} completed, adding label ---")
                    task_service.update_task(issue["id"], {"labels": [tags[0], "twerkflow-complete"]})

        return None

    def run_watcher(self, iterations: int = 0) -> None:
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
