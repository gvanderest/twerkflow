"""Defines the naive workflow graph."""

from langgraph.graph import END, StateGraph
from langchain_core.runnables import RunnableConfig
from src.core.state import TwerkflowState
from src.drivers.base import TaskService


def gate_check_tag(state: TwerkflowState, config: RunnableConfig) -> str:
    """Naive gate: check if 'twerkflow' tag exists."""
    tags = config["configurable"].get("tags", [])
    if "twerkflow" in tags:
        return "process"
    return "abort"


def process_task(state: TwerkflowState, config: RunnableConfig) -> TwerkflowState:
    """Agentic node: uses the injected TaskService to process a task."""
    ticket_id = config["configurable"].get("ticket_id")
    if not ticket_id:
        raise ValueError("Cannot process task without ticket_id")

    task_service: TaskService = config["configurable"]["task_service"]
    print(f"--- Real Driver Activity: Fetching task {ticket_id} ---")

    # This will trigger the NotImplementedError for now
    try:
        task_data = task_service.get_task(ticket_id)
        print(f"Task data: {task_data}")
    except NotImplementedError:
        print("Driver not fully implemented yet, skipping API call.")

    state.status = "processing"
    state.messages.append("Started processing")
    return state


def abort_task(state: TwerkflowState, config: RunnableConfig) -> TwerkflowState:
    """Node: aborts the task processing."""
    ticket_id = config["configurable"].get("ticket_id")
    print(f"Aborting task {ticket_id}...")
    state.status = "aborted"
    state.messages.append("Abort triggered")
    return state


# Assemble Graph
workflow = StateGraph(TwerkflowState)

workflow.add_node("process", process_task)
workflow.add_node("abort", abort_task)

workflow.set_conditional_entry_point(gate_check_tag, {"process": "process", "abort": "abort"})

workflow.add_edge("process", END)
workflow.add_edge("abort", END)

app = workflow.compile()
