from typing import List, Dict, Any

from langchain_core.tools import StructuredTool

from tools.finish import create_finish_tool
from tools.get_linkedin_profile_data import create_linkedin_profile_tool


class ToolRegistryService:
    def __init__(self):
        self._tools = None

    def get_tools(self) -> List[StructuredTool]:
        if self._tools is None:
            self._tools = [
                create_finish_tool(),
                create_linkedin_profile_tool()
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
