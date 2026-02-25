from config import Config

class ActionAgent(Config):

    SYSTEM_PROMPT = """
        You are a meeting action items agent. You will extract action items from
        the minutes of meeting.

        ROLE:
        1. Analyze the meeting transcript given by user in "User Input".
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

    def process(self, transcript: str) -> dict:
        return self.chain_prompt(self.SYSTEM_PROMPT + " User Input: " + transcript, "action_items")
        

        