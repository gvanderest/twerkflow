"""Defines the hydration workflow."""

import time
from langgraph.graph import END, StateGraph
from langchain_core.runnables import RunnableConfig
from src.core.state import TwerkflowState
from src.drivers.base import TaskService
from src.core.config_loader import load_settings
from src.workflows.experiment_flow import generate_fortune


def hydrate_issues(state: TwerkflowState, config: RunnableConfig) -> TwerkflowState:
    """Node: find tagged issues and hydrate state."""
    task_service: TaskService = config["configurable"]["task_service"]
    settings = load_settings()
    label = settings.get_driver_config("task_service").params.get("label_to_search")

    if not label:
        raise ValueError("label_to_search not configured for task_service")

    print(f"--- Hydrating issues with label: {label} ---")

    issues = task_service.list_issues_by_label(label)

    # Filter for un-hydrated issues
    unhydrated_issues = [i for i in issues if "<twerkflow>" not in i["body"]]

    if not unhydrated_issues:
        print("--- No un-hydrated issues found. ---")
        state.status = "no_issues"
    else:
        # Take the first one found
        issue = unhydrated_issues[0]
        print(f"--- Hydrating issue: {issue['id']} ---")

        # Populate state with discovery
        state.ticket_id = issue["id"]
        # Inject ticket_id into config dynamically
        config["configurable"]["ticket_id"] = state.ticket_id

        # PERSIST: Update the issue body with the state
        task_service.update_twerkflow_state(issue["id"], state)
        print(f"--- Persisted state to issue {issue['id']} ---")

        state.status = "starting"

    return state


def fortune_node(state: TwerkflowState, config: RunnableConfig) -> TwerkflowState:
    """Node: conditionally run fortune teller."""
    # The config is not shared between nodes, so we must rely on state.ticket_id
    ticket_id = state.ticket_id
    print(f"--- fortune_node: status={state.status}, ticket_id={ticket_id} ---")
    if state.status == "starting" and ticket_id:
        # Re-inject into config for generate_fortune
        config["configurable"]["ticket_id"] = ticket_id
        return generate_fortune(state, config)
    return state


def delay_node(state: TwerkflowState, config: RunnableConfig) -> TwerkflowState:
    """Node: delay before re-polling."""
    settings = load_settings()
    interval = settings.poll_interval_seconds
    # DI: Get sleep_func, default to time.sleep
    sleep_func = config["configurable"].get("sleep_func", time.sleep)

    print(f"--- Sleeping for {interval}s ---")
    sleep_func(interval)
    state.status = "pending"
    return state


def check_hydration_status(state: TwerkflowState) -> str:
    """Conditional edge: check if issues were hydrated."""
    print(f"--- check_hydration_status: state.status={state.status} ---")
    if state.status in ["starting", "completed"]:
        return "finished"
    return "delay"


# Assemble Graph
workflow = StateGraph(TwerkflowState)
workflow.add_node("hydrate", hydrate_issues)
workflow.add_node("fortune", fortune_node)
workflow.add_node("delay", delay_node)
workflow.set_entry_point("hydrate")

# Conditional edges to loop
workflow.add_conditional_edges("hydrate", check_hydration_status, {"finished": "fortune", "delay": "delay"})
workflow.add_edge("fortune", END)
workflow.add_edge("delay", "hydrate")

app = workflow.compile()
