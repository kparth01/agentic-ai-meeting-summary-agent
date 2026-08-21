from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

class LLMCall:

    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        self.temperature = os.getenv("TEMPERATURE", 0.7)
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.llm = self.get_llm()

    def get_llm(self):
        return ChatOpenAI(
            model = str(self.model),
            temperature = float(self.temperature),
            api_key = self.openai_api_key
        )


    def query_llm(self, system_msg: str, human_msg: str):

        messages = [
            {
                "role": "system",
                "content": system_msg
            },
            {
                "role": "user",
                "content": human_msg
            }
        ]

        response = self.llm.invoke(messages)
        return response.content


if __name__ == "__main__":
    llm = LLMCall()
    resp = llm.query_llm("You are helpful assistant", "What the weather today?")
    print(resp)



