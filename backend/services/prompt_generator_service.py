from typing import List, Dict, Any

from constants.prompts import AGENT_SYSTEM_PROMPT, FINISH_SYSTEM_PROMPT


class PromptGeneratorService:
    def __init__(self):
        pass

    def build_agent_context(self, user_goal: str, linkedin_profile_url: str) -> str:
        return f"""User's Goal: {user_goal}

LinkedIn Profile to Research: {linkedin_profile_url}

Please research this person and determine if their needs/pain points align with the user's goal. Use available tools to gather comprehensive information."""

    def build_final_summary_prompt(self, context: str) -> List[Dict[str, str]]:
        return [
            {"role": "system", "content": FINISH_SYSTEM_PROMPT},
            {"role": "user", "content": f"Based on the following research context, provide a concise assessment of intent alignment:\n\n{context}"}
        ]


service = PromptGeneratorService()
