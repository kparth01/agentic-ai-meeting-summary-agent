from config import Config
import json

class CombineAgent(Config):

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
                "summary": "<the summary here>",
                "action_items": "<Person>: <Action Items>"
            }}
        }}
    """

    def print(self, summary_output: str, action_items_output: list) -> dict: 
        llm_input = self.SYSTEM_PROMPT + "\n"
        
        # Explicitly tell the LLM what was requested
        if summary_output:
            llm_input += f"Summary Agent Output: {summary_output}\n"
        else:
            llm_input += "Summary Agent Output: NOT REQUESTED\n"
            
        if action_items_output:
            action_items_str = json.dumps(action_items_output)
            llm_input += f"Action Items Output: {action_items_str}\n"
        else:
            llm_input += "Action Items Output: NOT REQUESTED\n"

        if summary_output and action_items_output:
            action_items_str = json.dumps(action_items_output)
            llm_input += f"""Both summary and action items were requested. 
                            Summary Output: {summary_output}\n
                            Action Items Output: {action_items_str}\n"""
            
        return self.chain_prompt(llm_input, "combine_agent")