import asyncio
import json
from typing import AsyncGenerator, Dict, Any, List

from constants.prompts import AGENT_SYSTEM_PROMPT
from services.openai_service import service as openai_service
from services.prompt_generator_service import service as prompt_service
from services.tool_registry_service import service as tool_registry_service
from tools.finish import finish_execution
from tools.get_linkedin_profile_data import get_linkedin_profile_data
from tools.get_linkedin_profile_posts import get_linkedin_profile_posts
from tools.get_linkedin_profile_reactions import get_linkedin_profile_reactions
from tools.get_linkedin_company_details import get_linkedin_company_details
from tools.get_linkedin_company_posts import get_linkedin_company_posts
from tools.browse_web import browse_web
from tools.analyze_with_llm import analyze_with_llm
from tools.search_web import search_web
from tools.search_company_news import search_company_news
from tools.search_person_news import search_person_news

class ToolCallingService:
    def __init__(self):
        self.max_iterations = 10
        self._tool_map = {
            "finish": finish_execution,
            "get_linkedin_profile_data": get_linkedin_profile_data,
            "get_linkedin_profile_posts": get_linkedin_profile_posts,
            "get_linkedin_profile_reactions": get_linkedin_profile_reactions,
            "get_linkedin_company_details": get_linkedin_company_details,
            "get_linkedin_company_posts": get_linkedin_company_posts,
            "browse_web": browse_web,
            "analyze_with_llm": analyze_with_llm,
            "search_web": search_web,
            "search_company_news": search_company_news,
            "search_person_news": search_person_news
        }

    async def execute_with_streaming(
        self,
        user_goal: str,
        linkedin_profile_url: str
    ) -> AsyncGenerator[str, None]:
        messages = [
            {"role": "system", "content": AGENT_SYSTEM_PROMPT},
            {"role": "user", "content": prompt_service.build_agent_context(user_goal, linkedin_profile_url)}
        ]

        tools = tool_registry_service.get_tools_as_openai_format()

        yield f"data: {json.dumps({'type': 'started', 'message': 'Agent execution started'})}\n\n"

        try:
            for iteration in range(self.max_iterations):
                yield f"data: {json.dumps({'type': 'iteration', 'iteration': iteration + 1})}\n\n"

                response = await openai_service.create_chat_completion_with_tools_async(
                    messages=messages,
                    tools=tools,
                    temperature=0.7
                )

                assistant_message = response.choices[0].message

                if not assistant_message.tool_calls:
                    yield f"data: {json.dumps({'type': 'no_tool_call', 'message': assistant_message.content or 'Agent finished without calling tools'})}\n\n"
                    break

                messages.append({
                    "role": "assistant",
                    "content": assistant_message.content,
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": tc.type,
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments
                            }
                        } for tc in assistant_message.tool_calls
                    ]
                })

                should_finish = False

                for tool_call in assistant_message.tool_calls:
                    tool_name = tool_call.function.name
                    tool_args = json.loads(tool_call.function.arguments)

                    yield f"data: {json.dumps({'type': 'tool_started', 'tool_name': tool_name, 'arguments': tool_args})}\n\n"

                    if tool_name not in self._tool_map:
                        error_result = {"error": f"Unknown tool: {tool_name}"}
                        yield f"data: {json.dumps({'type': 'tool_error', 'error': error_result})}\n\n"
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": json.dumps(error_result)
                        })
                        continue

                    tool_func = self._tool_map[tool_name]
                    result = await asyncio.to_thread(tool_func, **tool_args)

                    yield f"data: {json.dumps({'type': 'tool_completed', 'tool_name': tool_name, 'result': result})}\n\n"

                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(result)
                    })

                    if tool_name == "finish":
                        should_finish = True

                if should_finish:
                    final_summary = await self._generate_final_summary(messages)
                    yield f"data: {json.dumps({'type': 'final_result', 'summary': final_summary})}\n\n"
                    break

            else:
                yield f"data: {json.dumps({'type': 'max_iterations', 'message': 'Reached maximum iterations'})}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

    async def _generate_final_summary(self, messages: List[Dict[str, Any]]) -> str:
        context_summary = self._extract_context_summary(messages)

        summary_messages = prompt_service.build_final_summary_prompt(context_summary)

        final_summary = await openai_service.create_chat_completion_async(
            messages=summary_messages,
            temperature=0.3
        )

        return final_summary

    def _extract_context_summary(self, messages: List[Dict[str, Any]]) -> str:
        context_parts = []

        for msg in messages:
            if msg["role"] == "user":
                context_parts.append(f"User Request: {msg['content']}")
            elif msg["role"] == "tool":
                context_parts.append(f"Tool Result: {msg['content']}")

        return "\n\n".join(context_parts)


service = ToolCallingService()
