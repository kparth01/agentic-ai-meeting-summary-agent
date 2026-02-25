import os
from langgraph.graph import StateGraph, START, END

import json
from state import AgentState
from agents.actionAgent import ActionAgent
from agents.summaryAgent import SummaryAgent
from agents.supervisorAgent import SupervisorAgent
from agents.combineAgent import CombineAgent

# Init Agents
supervisor = SupervisorAgent()
summary = SummaryAgent()
actions = ActionAgent()
combine = CombineAgent()

def supervisor_flow(state: AgentState) -> dict:
    print("Analyzing user input to understand their intent...")
    user_input = state["user_input"]
    transcript = state["transcript"]
    result = supervisor.oversee(user_input, transcript)
    return {"supervisor_agent": result["supervisor_agent"]}

def summary_flow(state: AgentState) -> dict:
    print("Generating summary of the meeting...")
    result = summary.process(state["transcript"])
    return {"summary_agent": result["summary_agent"]}

def action_flow(state: AgentState) -> dict:
    print("Identifying action items for each individual in the meeting...")
    result = actions.process(state["transcript"])
    return {"action_items": result["action_items"]}

def combine_flow(state: AgentState) -> dict:
    summary_output = ""
    action_items_output = []
    if "summary_items" in state["supervisor_agent"]:
        ip = state["summary_agent"]
        json_data = json.loads(ip)
        summary_output = json_data.get("summary", "").lower()
    
    if "action_items" in state["supervisor_agent"]:
        actions_ip = state["action_items"]
        actions_data = json.loads(actions_ip)
        action_items_output = actions_data.get("actions", [])
    
    result = combine.print(summary_output, action_items_output)
    
    return {"combine": result["combine_agent"]}


def route_planner(state: AgentState) -> list[str]:
    supervisor_output = state["supervisor_agent"]
    nodes = []
    if "summary_items" in supervisor_output:
        nodes.append("summary_agent")
    if "action_items" in supervisor_output:
       nodes.append("action_items")
    return nodes

def create_workflow():
    builder = StateGraph(AgentState)

    builder.add_node("supervisor_agent", supervisor_flow)
    builder.add_node("summary_agent", summary_flow)
    builder.add_node("action_items", action_flow)
    builder.add_node("combine", combine_flow)

    builder.add_edge(START, "supervisor_agent")

    builder.add_conditional_edges("supervisor_agent", 
        route_planner,
        {
            "summary_agent": "summary_agent",
            "action_items": "action_items",
        }
    )

    builder.add_edge("summary_agent", "combine")
    builder.add_edge("action_items", "combine")

    builder.add_edge("combine", END)

    return builder.compile()

app = create_workflow()