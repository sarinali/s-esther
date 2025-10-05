from typing import Dict, Any

from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

from services.openai_service import service as openai_service


class AnalyzeWithLLMInput(BaseModel):
    prompt: str = Field(description="The analysis prompt/question to ask the LLM")
    context: str = Field(description="The context or data to analyze")


def analyze_with_llm(prompt: str, context: str) -> str:
    result = openai_service.analyze_with_reasoning(prompt, context)
    return result


def create_analyze_with_llm_tool() -> StructuredTool:
    return StructuredTool.from_function(
        func=analyze_with_llm,
        name="analyze_with_llm",
        description="Use a reasoning LLM (o3-mini with medium reasoning) to deeply analyze content. Perfect for extracting BANT signals, sentiment analysis, pattern recognition, or complex insights from scraped data. Provide a clear analysis prompt and the context to analyze.",
        args_schema=AnalyzeWithLLMInput
    )
