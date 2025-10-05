import asyncio
import json
from typing import AsyncGenerator, Dict, Any, List

from constants.prompts import AGENT_SYSTEM_PROMPT
from constants.tool_metadata import TOOL_METADATA
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

                    tool_metadata = TOOL_METADATA.get(tool_name, {
                        "title": tool_name.replace("_", " ").title(),
                        "description": f"Executing {tool_name}"
                    })

                    yield f"data: {json.dumps({'type': 'tool_started', 'tool_name': tool_name, 'tool_title': tool_metadata['title'], 'tool_description': tool_metadata['description'], 'arguments': tool_args})}\n\n"

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
                        research_summary = result.get("summary", "")

                if should_finish:
                    final_assessment = await self._generate_final_assessment(research_summary, user_goal, messages)
                    yield f"data: {json.dumps({'type': 'final_result', 'assessment': final_assessment})}\n\n"
                    break

            else:
                yield f"data: {json.dumps({'type': 'max_iterations', 'message': 'Reached maximum iterations'})}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

    async def _generate_final_assessment(self, research_summary: str, user_goal: str, message_context: str) -> Dict[str, Any]:
        max_retries = 3

        for attempt in range(max_retries):
            scoring_result = await asyncio.to_thread(
                openai_service.score_prospect,
                research_summary,
                user_goal,
                message_context
            )

            try:
                assessment = json.loads(scoring_result)

                if all(key in assessment for key in ["good_signals", "bad_signals", "score", "reasoning"]):
                    return assessment
                else:
                    if attempt < max_retries - 1:
                        continue

            except json.JSONDecodeError:
                if attempt < max_retries - 1:
                    continue

        return {
            "good_signals": [],
            "bad_signals": [],
            "score": 50,
            "reasoning": "Error parsing assessment after 3 retries",
            "raw_response": scoring_result
        }

    def _extract_context_summary(self, messages: List[Dict[str, Any]]) -> str:
        context_parts = []

        for msg in messages:
            if msg["role"] == "user":
                context_parts.append(f"User Request: {msg['content']}")
            elif msg["role"] == "tool":
                context_parts.append(f"Tool Result: {msg['content']}")

        return "\n\n".join(context_parts)


service = ToolCallingService()
