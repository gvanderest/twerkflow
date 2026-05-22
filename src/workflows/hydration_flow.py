"""Defines the hydration workflow."""

from langgraph.graph import END, StateGraph
from langchain_core.runnables import RunnableConfig
from src.core.state import TwerkflowState
from src.drivers.base import TaskService
from src.core.config_loader import load_settings


def hydrate_issues(state: TwerkflowState, config: RunnableConfig) -> TwerkflowState:
    """Node: find tagged issues and hydrate state."""
    task_service: TaskService = config["configurable"]["task_service"]
    # Get config for the task_service
    # We are assuming it's GitHubIssueTaskService here for this demo
    # In a more robust system, we would get the config from the DriverFactory

    # Let's inspect the driver to see how to get the config
    # Actually, the driver doesn't store its config, it only gets it via init.
    # To get the label, we need the driver to have been initialized with the config.
    # Or we can get it from settings via DriverFactory.

    # For now, let's just get it from settings globally as a hack
    settings = load_settings()
    label = settings.get_driver_config("task_service").params.get("label_to_search")

    if not label:
        raise ValueError("label_to_search not configured for task_service")

    print(f"--- Hydrating issues with label: {label} ---")

    issues = task_service.list_issues_by_label(label)

    for issue in issues:
        print(f"Checking issue: {issue['id']}")
        # In a real hydration scenario, we'd check if the state block exists
        # and if not, initialize it.
        # This is a proof-of-work: just find and log.

    state.status = "hydrated"
    return state


# Assemble Graph
workflow = StateGraph(TwerkflowState)
workflow.add_node("hydrate", hydrate_issues)
workflow.set_entry_point("hydrate")
workflow.add_edge("hydrate", END)

app = workflow.compile()
