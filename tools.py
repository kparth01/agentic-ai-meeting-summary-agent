import os
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv

load_dotenv()

_transcript: str = ""

def set_transcript(transcript: str) -> None:
    global _transcript
    _transcript = transcript

def _llm() -> ChatOpenAI:
    return ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0,
        openai_api_key=os.getenv("OPENAI_API_KEY"),
    )

@tool
def summarize_meeting() -> str:
    """Generate a concise summary of the meeting transcript (8-10 sentences)."""
    print("  → tool: summarize_meeting")
    response = _llm().invoke([
        SystemMessage(content="You are a meeting summarizer. Return a clear, concise summary of 8-10 sentences covering key decisions and discussions."),
        HumanMessage(content=f"Transcript:\n{_transcript}"),
    ])
    return response.content

@tool
def extract_action_items() -> str:
    """Extract action items and their owners from the meeting transcript."""
    print("  → tool: extract_action_items")
    response = _llm().invoke([
        SystemMessage(content="You are an action items extractor. List every action item and the person responsible in a clear, readable format."),
        HumanMessage(content=f"Transcript:\n{_transcript}"),
    ])
    return response.content
