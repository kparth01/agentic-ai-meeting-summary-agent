from typing import TypedDict

class AgentState(TypedDict):
    user_input: str
    intent: str
    summary: str
    action: dict
    transcript: str
    summary_and_action: str
    final_response: dict
