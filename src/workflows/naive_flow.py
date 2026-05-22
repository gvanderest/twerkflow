from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableConfig
from src.core.state import TwerkflowState
from src.drivers.base import TaskService


# Naive gate: check if 'twerkflow' tag exists
def gate_check_tag(state: TwerkflowState, config: RunnableConfig):
    if "twerkflow" in state.tags:
        return "process"
    return "abort"


# Agentic node: uses the injected TaskService
def process_task(state: TwerkflowState, config: RunnableConfig):
    task_service: TaskService = config["configurable"]["task_service"]
    print(f"--- Real Driver Activity: Fetching task {state.ticket_id} ---")
    
    # This will trigger the NotImplementedError for now
    try:
        task_data = task_service.get_task(state.ticket_id)
        print(f"Task data: {task_data}")
    except NotImplementedError:
        print("Driver not fully implemented yet, skipping API call.")

    state.status = "processing"
    state.messages.append("Started processing")
    return state


# Node: abort
def abort_task(state: TwerkflowState, config: RunnableConfig):
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
