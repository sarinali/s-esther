from typing import List, Dict, Any

from langchain_core.tools import StructuredTool

from tools.analyze_with_llm import create_analyze_with_llm_tool
from tools.browse_web import create_browse_web_tool
from tools.finish import create_finish_tool
from tools.get_linkedin_company_details import create_linkedin_company_details_tool
from tools.get_linkedin_company_posts import create_linkedin_company_posts_tool
from tools.get_linkedin_profile_data import create_linkedin_profile_tool
from tools.get_linkedin_profile_posts import create_linkedin_profile_posts_tool
from tools.get_linkedin_profile_reactions import create_linkedin_profile_reactions_tool
from tools.search_company_news import create_search_company_news_tool
from tools.search_person_news import create_search_person_news_tool
from tools.search_web import create_search_web_tool


class ToolRegistryService:
    def __init__(self):
        self._tools = None

    def get_tools(self) -> List[StructuredTool]:
        if self._tools is None:
            self._tools = [
                create_finish_tool(),
                create_linkedin_profile_tool(),
                create_linkedin_profile_posts_tool(),
                create_linkedin_profile_reactions_tool(),
                create_linkedin_company_details_tool(),
                create_linkedin_company_posts_tool(),
                create_browse_web_tool(),
                create_search_web_tool(),
                create_search_company_news_tool(),
                create_search_person_news_tool(),
                create_analyze_with_llm_tool()
            ]

        return self._tools

    def get_tools_as_openai_format(self) -> List[Dict[str, Any]]:
        tools = self.get_tools()
        openai_tools = []

        for tool in tools:
            openai_tool = {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.args_schema.model_json_schema()
                }
            }
            openai_tools.append(openai_tool)

        return openai_tools


service = ToolRegistryService()
