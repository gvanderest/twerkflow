from langgraph.graph import StateGraph, END
from src.core.state import TwerkflowState


# Naive gate: check if 'twerkflow' tag exists
def gate_check_tag(state: TwerkflowState):
    if "twerkflow" in state.tags:
        return "process"
    return "abort"


# Agentic node: dummy node for now
def process_task(state: TwerkflowState):
    print(f"Processing task {state.ticket_id}...")
    state.status = "processing"
    state.messages.append("Started processing")
    return state


# Node: abort
def abort_task(state: TwerkflowState):
    print(f"Aborting task {state.ticket_id}...")
    state.status = "aborted"
    state.messages.append("Abort triggered")
    return state


# Assemble Graph
workflow = StateGraph(TwerkflowState)

workflow.add_node("process", process_task)
workflow.add_node("abort", abort_task)

workflow.set_conditional_entry_point(
    gate_check_tag,
    {
        "process": "process",
        "abort": "abort"
    }
)

workflow.add_edge("process", END)
workflow.add_edge("abort", END)

app = workflow.compile()
