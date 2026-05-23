"""Defines an experimental workflow for fortune teller."""

from typing import cast
from langgraph.graph import END, StateGraph
from langchain_core.runnables import RunnableConfig
from src.core.state import TwerkflowState
from src.core.types import WorkflowConfig


def start_node(state: TwerkflowState, config: RunnableConfig) -> TwerkflowState:
    """Initializes the workflow."""
    print("--- Starting fortune workflow ---")
    state.status = "starting"
    return state


def generate_fortune(state: TwerkflowState, config: RunnableConfig) -> TwerkflowState:
    """Runs pi to generate fortune and comments it."""
    conf = cast(WorkflowConfig, config["configurable"])
    ticket_id = conf.get("ticket_id")
    if not ticket_id:
        raise ValueError("Cannot process task without ticket_id")

    runner = conf["command_runner"]
    task_service = conf["task_service"]

    print(f"--- Generating fortune for issue {ticket_id} ---")

    # Run pi headless
    cmd = ["pi", "-p", "--model", "google/gemini-flash-lite-latest", "give me a fortune, 50 characters or less"]
    fortune = runner.run(cmd)
    print(f"--- Fortune: {fortune} ---")

    # Comment fortune
    comment_cmd = [
        "gh",
        "issue",
        "comment",
        ticket_id,
        "-b",
        f"{fortune} \n\n --- *Authored by Twerkflow (experimental)* ---",
    ]
    runner.run(comment_cmd)

    state.status = "completed"

    # Persist state
    task_service.update_twerkflow_state(ticket_id, state)

    return state


def check_status(state: TwerkflowState) -> str:
    """Conditional edge: check if completed."""
    if state.status == "completed":
        return "end"
    return "process"


# Assemble Graph
workflow = StateGraph(TwerkflowState)
workflow.add_node("start", start_node)
workflow.add_node("process", generate_fortune)

workflow.set_entry_point("start")
workflow.add_edge("start", "process")
workflow.add_edge("process", END)

app = workflow.compile()
