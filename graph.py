from langgraph.graph import StateGraph, START, END
from supervisor.state import AgentState

from supervisor.orchestrator import Orchestrator

orchestrator = Orchestrator()

def orchestrator_node(state: AgentState):
    user_input = state["user_input"]
    print(f"Orchestrator invoked {user_input}")

def create_graph():
    graph = StateGraph(AgentState)

    graph.add_node("orchestrator", orchestrator_node)

    graph.add_edge(START, "orchestrator")
    graph.add_edge("orchestrator", END)

    return graph.compile()

graph = create_graph()