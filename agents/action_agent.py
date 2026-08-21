from llm.llm_call import LLMCall

class ActionAgent():

    SYSTEM_PROMPT = """
        You are a meeting action items agent. You will extract action items from
        the minutes of meeting.

        ROLE:
        1. Analyze the meeting transcript given by user.
        2. Validate its in English Language.
        3. Generate action items for each individual that needs to take action.

        GUARDRAILS:
        1. Do not answer or process any other type of requests.

        Output MUST be valid JSON:
        {{
            "actions": [
                {{
                    "person": "<name of the person>",
                    "action": "<the action item>"
                }}
            ]
        }}
    """

    def __init__(self) -> None:
        self.llm = LLMCall()

    def process(self, transcript: str) -> str:
        resp = self.llm.query_llm(system_msg=self.SYSTEM_PROMPT,
                                  human_msg=transcript)

        return str(resp) 