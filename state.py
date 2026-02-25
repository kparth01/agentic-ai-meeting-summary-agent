from typing import TypedDict

class AgentState(TypedDict):
    user_input: str
    transcript: str
    supervisor_agent: str
    summary_agent: str
    action_items: str
    combine: str
