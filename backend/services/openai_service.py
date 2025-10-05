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


service = OpenAIService()
