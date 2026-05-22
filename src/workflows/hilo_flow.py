"""Defines the HILO workflow graph with polling capability."""

import time
from langgraph.graph import END, StateGraph
from langchain_core.runnables import RunnableConfig
from src.core.state import TwerkflowState
from src.core.config_loader import load_settings
from src.drivers.base import TaskService


def gate_check_tag(state: TwerkflowState, config: RunnableConfig) -> str:
    """Gate: check if 'twerkflow' tag exists."""
    if "twerkflow" in state.tags:
        return "process"
    return "abort"


def process_task(state: TwerkflowState, config: RunnableConfig) -> TwerkflowState:
    """Agentic node: processes a task."""
    print(f"--- Processing task {state.ticket_id} ---")
    state.status = "processing"
    state.messages.append("Started processing")
    return state


def check_approval(state: TwerkflowState, config: RunnableConfig) -> str:
    """Helper: checks for approval."""
    if not state.ticket_id:
        return "pending"

    task_service: TaskService = config["configurable"]["task_service"]
    comments = task_service.get_comments(state.ticket_id)
    for comment in comments:
        if "twerkflow approve" in comment["body"].lower():
            return "approved"
    return "pending"


def polling_node(state: TwerkflowState, config: RunnableConfig) -> TwerkflowState:
    """Polling node: checks for approval, sleeps if not approved."""
    # DI: Get dependencies from config or injected services
    # We use .get() to allow defaults, ensuring backward compatibility if config is missing
    settings = config["configurable"].get("settings") or load_settings()
    sleep_func = config["configurable"].get("sleep_func", time.sleep)

    interval = settings.poll_interval_seconds

    print(f"--- Polling for approval for task {state.ticket_id} ---")

    action = check_approval(state, config)
    if action == "approved":
        print("--- Approval detected! ---")
        state.status = "approved"
    else:
        print(f"--- No approval yet. Sleeping for {interval}s ---")
        sleep_func(interval)
        state.status = "pending"
    return state


def check_polling_status(state: TwerkflowState) -> str:
    """Conditional edge: checks state to determine next node."""
    if state.status == "approved":
        return "approved"
    return "pending"


def finalize_task(state: TwerkflowState, config: RunnableConfig) -> TwerkflowState:
    """Node: finalizes the task."""
    print(f"--- Finalizing task {state.ticket_id} ---")
    state.status = "done"
    state.messages.append("Task finalized")
    return state


def abort_task(state: TwerkflowState, config: RunnableConfig) -> TwerkflowState:
    """Node: aborts the task processing."""
    print(f"Aborting task {state.ticket_id}...")
    state.status = "aborted"
    state.messages.append("Abort triggered")
    return state


# Assemble Graph
workflow = StateGraph(TwerkflowState)

workflow.add_node("process", process_task)
workflow.add_node("polling", polling_node)
workflow.add_node("finalize", finalize_task)
workflow.add_node("abort", abort_task)

workflow.set_conditional_entry_point(gate_check_tag, {"process": "process", "abort": "abort"})

# Define the polling loop: process -> polling -> polling (if pending) OR finalize (if approved)
workflow.add_edge("process", "polling")

# Polling edges: check state to decide routing
workflow.add_conditional_edges("polling", check_polling_status, {"approved": "finalize", "pending": "polling"})

workflow.add_edge("finalize", END)
workflow.add_edge("abort", END)

app = workflow.compile()
