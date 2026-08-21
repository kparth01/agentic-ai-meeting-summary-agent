import json
from langgraph.graph import StateGraph, START, END
from supervisor.state import AgentState

from supervisor.orchestrator import Orchestrator
from agents.summary_agent import SummaryAgent
from agents.action_agent import ActionAgent
from supervisor.aggregator import Aggregator
from formatter import OutputFormatter

orchestrator = Orchestrator()
summary_agent = SummaryAgent()
action_agent = ActionAgent()
aggregator = Aggregator()
output_formatter = OutputFormatter

def orchestrator_node(state: AgentState):
    user_input = state["user_input"]
    raw = orchestrator.find_intent(user_input=user_input)
    intent = raw.strip().strip('"')
    return { "intent": intent }


def summary_node(state: AgentState):
    transcript = state["transcript"]
    generated_summary = summary_agent.process(transcript=transcript)
    return { "summary": generated_summary }


def action_node(state: AgentState):
    transcript = state["transcript"]
    generated_actions = action_agent.process(transcript=transcript)
    return { "action": generated_actions }


def summary_and_action_node(state: AgentState):
    transcript = state["transcript"]
    generated_summary = summary_agent.process(transcript=transcript)
    generated_actions = action_agent.process(transcript=transcript)
    result = f"Summary: {generated_summary} Actions: {generated_actions}"
    return { "summary_and_action": result }


def route_intent(state: AgentState) -> str:
    intent = state["intent"]
    if intent == "summary_items":
        return "summary"
    elif intent == "action_items":
        return "action"
    elif intent == "summary_and_action_items":
        return "summary_and_action" 


def aggregator_node(state: AgentState):
    intent = state["intent"]
    final_input = ""
    if intent == "summary_items":
        final_input = f"SUMMARY ONLY (do not include action items):\n{state['summary']}"
    elif intent == "action_items":
        final_input = f"ACTION ITEMS ONLY (do not include summary):\n{json.dumps(state['action'])}"
    elif intent == "summary_and_action_items":
        final_input = state["summary_and_action"]

    result = aggregator.print(input_data=final_input)
    return { "final_response": result }



def create_graph():
    graph = StateGraph(AgentState)

    graph.add_node("orchestrator", orchestrator_node)
    graph.add_node("summary", summary_node)
    graph.add_node("action", action_node)
    graph.add_node("summary_and_action", summary_and_action_node)
    graph.add_node("aggregator", aggregator_node)

    graph.add_edge(START, "orchestrator")
    graph.add_conditional_edges(
        "orchestrator",         
        route_intent,            
        {
            "summary": "summary",
            "action":  "action",
            "summary_and_action": "summary_and_action"
        }
    )
    graph.add_edge("summary", "aggregator")
    graph.add_edge("action", "aggregator")
    graph.add_edge("summary_and_action", "aggregator")

    graph.add_edge("aggregator", END)

    return graph.compile()

graph = create_graph()