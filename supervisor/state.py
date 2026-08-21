from typing import TypedDict

class AgentState(TypedDict):
    user_input: str
    intent: str
    summary: str
    action: str
    transcript: str
    summary_and_action: str
    final_response: dict
