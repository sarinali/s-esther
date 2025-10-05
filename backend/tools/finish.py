from typing import Dict, Any

from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field


class FinishInput(BaseModel):
    summary: str = Field(description="A summary of what was accomplished in this agent execution")


def finish_execution(summary: str) -> Dict[str, Any]:
    return {
        "status": "completed",
        "summary": summary,
        "action": "finish"
    }


def create_finish_tool() -> StructuredTool:
    return StructuredTool.from_function(
        func=finish_execution,
        name="finish",
        description="Indicate that the task is complete and return a summary of what was accomplished. Use this when you have finished all required actions.",
        args_schema=FinishInput
    )
