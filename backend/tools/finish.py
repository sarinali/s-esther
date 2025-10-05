from typing import Dict, Any

from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field


class FinishInput(BaseModel):
    summary: str = Field(description="Comprehensive summary of all research findings, including key insights from LinkedIn and web sources")


def finish_execution(summary: str) -> Dict[str, Any]:
    return {
        "status": "completed",
        "action": "finish",
        "summary": summary
    }


def create_finish_tool() -> StructuredTool:
    return StructuredTool.from_function(
        func=finish_execution,
        name="finish",
        description="Complete the research task with a comprehensive summary of findings. Include all relevant information discovered from LinkedIn and web sources.",
        args_schema=FinishInput
    )
