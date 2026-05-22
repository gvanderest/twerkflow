"""Defines the hydration workflow."""

import time
from langgraph.graph import END, StateGraph
from langchain_core.runnables import RunnableConfig
from src.core.state import TwerkflowState
from src.drivers.base import TaskService
from src.core.config_loader import load_settings
from src.workflows.experiment_flow import generate_fortune


def hydrate_issues(state: TwerkflowState, config: RunnableConfig) -> TwerkflowState:
    """Node: persist initial state to the found issue."""
    task_service: TaskService = config["configurable"]["task_service"]
    ticket_id = config["configurable"].get("ticket_id")

    if not ticket_id:
        raise ValueError("Cannot hydrate issue without ticket_id")

    print(f"--- Persisting initial state to issue {ticket_id} ---")

    # PERSIST: Update the issue body with the state
    task_service.update_twerkflow_state(ticket_id, state)

    state.status = "starting"

    return state


def fortune_node(state: TwerkflowState, config: RunnableConfig) -> TwerkflowState:
    """Node: conditionally run fortune teller."""
    # Rely on context in state
    ticket_id = state.context.get("ticket_id")
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
