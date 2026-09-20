from llm.llm_call import LLMCall

class SentimentAgent():

    SYSTEM_PROMPT = """
        You are a meeting sentiment agent. You must derive the sentiment of the meeting in 
        following categories only.
            1. Positive
            2. Negative
            3. Neutral

            
        ROLE:
        1. You are an expert in sentiment analysis.
        2. Analyze the meeting transcript given by user.
        3. Validate its in English Language.

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
        

        