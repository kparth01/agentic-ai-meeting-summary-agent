import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

class Config:

    def __init__(self) -> None:
        self.llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"), 
                            temperature=os.getenv("TEMPERATURE"),
                            openai_api_key=os.getenv("OPENAI_API_KEY"))


    def chain_prompt(self, prompts: str, stateStep: str) -> dict:
        # Split system prompt from user input
        # First part (until "User Input:") is system/guidelines
        # Rest is user input/data
        if "User Input:" in prompts:
            parts = prompts.split("User Input:", 1)
            system_prompt = parts[0].strip()
            user_input = "User Input:" + parts[1]
        elif "Summary Agent Output:" in prompts or "Action Items Output:" in prompts:
            parts = prompts.split("Summary Agent Output:", 1)
            system_prompt = parts[0].strip()
            user_input = "Summary Agent Output:" + parts[1] if len(parts) > 1 else prompts
        else:
            # Fallback
            system_prompt = ""
            user_input = prompts
        
        # Build messages with proper separation
        messages = []
        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))
        messages.append(HumanMessage(content=user_input))
        
        chain = self.llm | StrOutputParser()
        result = chain.invoke(messages)
        return {
            stateStep: result
        }