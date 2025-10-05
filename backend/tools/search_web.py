from typing import Dict, Any, Optional

from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

from services.google_search_service import service as google_search_service


class SearchWebInput(BaseModel):
    query: str = Field(description="The search query to execute")
    num_results: int = Field(default=10, description="Number of results to return (max 10, default 10)")


def search_web(query: str, num_results: int = 10) -> Optional[Dict[str, Any]]:
    results = google_search_service.search(query, num_results)

    if not results:
        return {"error": "Failed to execute search", "query": query}

    return results


def create_search_web_tool() -> StructuredTool:
    return StructuredTool.from_function(
        func=search_web,
        name="search_web",
        description="Search the web using Google Custom Search. Returns search results with titles, links, and snippets. Perfect for finding information about companies, news, funding announcements, or any general research. Use browse_web to fetch full HTML of specific URLs.",
        args_schema=SearchWebInput
    )
