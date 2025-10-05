from typing import List, Dict, Any, Optional

from openai import OpenAI, AsyncOpenAI

from config import config


class OpenAIService:
    def __init__(self):
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        self.async_client = AsyncOpenAI(api_key=config.OPENAI_API_KEY)

    def create_chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = "gpt-4o-mini",
        temperature: float = 0.7,
        stream: bool = False,
        **kwargs
    ) -> Any:
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            stream=stream,
            **kwargs
        )

        if stream:
            return response

        return response.choices[0].message.content

    async def create_chat_completion_async(
        self,
        messages: List[Dict[str, str]],
        model: str = "gpt-4o-mini",
        temperature: float = 0.7,
        stream: bool = False,
        **kwargs
    ) -> Any:
        response = await self.async_client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            stream=stream,
            **kwargs
        )

        if stream:
            return response

        return response.choices[0].message.content

    async def create_chat_completion_with_tools_async(
        self,
        messages: List[Dict[str, Any]],
        tools: List[Dict[str, Any]],
        model: str = "gpt-4o",
        temperature: float = 0.7,
        stream: bool = False
    ) -> Any:
        response = await self.async_client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            temperature=temperature,
            stream=stream
        )

        if stream:
            return response

        return response

    def analyze_with_reasoning(
        self,
        prompt: str,
        context: str
    ) -> str:
        messages = [
            {
                "role": "user",
                "content": f"{prompt}\n\nContext:\n{context}"
            }
        ]

        response = self.client.chat.completions.create(
            model="o3-mini",
            messages=messages,
            reasoning_effort="medium"
        )

        return response.choices[0].message.content

    def score_prospect(
        self,
        research_summary: str,
        user_goal: str,
        message_context: List[Dict[str, str]]
    ) -> str:
        from constants.prompts import SCORING_SYSTEM_PROMPT

        messages = [
            {"role": "system", "content": SCORING_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"User's Product/Goal: {user_goal}\n\nResearch Findings:\n{research_summary}"
            }
        ]

        messages.extend(message_context)

        response = self.client.chat.completions.create(
            model="o3-mini",
            messages=messages,
            reasoning_effort="medium"
        )

        return response.choices[0].message.content


service = OpenAIService()
