from llm.llm_call import LLMCall
import json

class Aggregator():

    SYSTEM_PROMPT = """
        You are expert aggregator. You will combine the outputs of summary agent and 
        action items agent to create a final comprehensive report.

        ROLE:
        1. Combine both the outputs in a coherent manner.
        2. Ensure the final output is concise and captures all key points.
        3. If summary is empty or "not requested", omit it from output.
        4. If action items are empty or "not requested", omit them from output.

        GUARDRAILS:
        1. Do not answer or process any other type of requests.
        2. Output ONLY what was provided. Do NOT make up or generate content.
        3. If only summary is provided, output only the summary section.
        4. If only action items are provided, output only the action items section.

        Output MUST be valid JSON (remove sections that are empty):
        {{
            "final_aggregated_output": {{
                "summary": "SUMMARY_TEXT",
                "action_items": [
                    {{"person": "PERSON_NAME", "action": "ACTION_DESCRIPTION"}}
                ]
            }}
        }}
    """

    def __init__(self) -> None:
        self.llm = LLMCall()

    def print(self, input_data: str) -> dict: 
        resp = self.llm.query_llm(system_msg=self.SYSTEM_PROMPT, human_msg=input_data)
        return json.loads(resp)
        
        