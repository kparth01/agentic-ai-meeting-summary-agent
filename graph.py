import os
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from dotenv import load_dotenv

load_dotenv()

from tools import summarize_meeting, extract_action_items

TOOLS = [summarize_meeting, extract_action_items]

llm = ChatOpenAI(
    model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
    temperature=0,
    openai_api_key=os.getenv("OPENAI_API_KEY"),
).bind_tools(TOOLS)

SYSTEM_PROMPT = """You are a meeting assistant with two tools:
- summarize_meeting: generates a concise summary of the meeting
- extract_action_items: extracts action items and their owners

Call the appropriate tool(s) based on what the user asks for, then present the results clearly."""


def call_model(state: MessagesState) -> dict:
    messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}


tool_node = ToolNode(TOOLS)


def create_workflow():
    builder = StateGraph(MessagesState)

    builder.add_node("agent", call_model)
    builder.add_node("tools", tool_node)

    builder.add_edge(START, "agent")
    builder.add_conditional_edges("agent", tools_condition)
    builder.add_edge("tools", "agent")

    return builder.compile()


app = create_workflow()
