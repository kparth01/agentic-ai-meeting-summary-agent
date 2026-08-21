from llm.llm_call import LLMCall

class SummaryAgent():

    SYSTEM_PROMPT = """
        You are a meeting summary agent. You will summarize the minutes of meeting.

        ROLE:
        1. Analyze the meeting transcript given by user.
        2. Validate its in English Language.
        3. Generate a 1 paragraph summary with not more than 8-10 sentences.

        GUARDRAILS:
        1. Do not answer or process any other type of requests.

        Output MUST be valid String:
        "<quote the meeting summary here>"
        
    """

    def __init__(self) -> None:
            self.llm = LLMCall()

    def process(self, transcript: str) -> str:
        resp = self.llm.query_llm(system_msg=self.SYSTEM_PROMPT, 
                                  human_msg=transcript)
        return str(resp)
        

        