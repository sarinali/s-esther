from typing import Dict, Any, Optional

from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

from services.web_browsing_service import service as web_browsing_service


class BrowseWebInput(BaseModel):
    url: str = Field(description="The URL to fetch and browse")


def browse_web(url: str) -> Optional[Dict[str, Any]]:
    result = web_browsing_service.fetch_url(url)

    if not result:
        return {"error": "Failed to fetch URL", "url": url}

    return result


def create_browse_web_tool() -> StructuredTool:
    return StructuredTool.from_function(
        func=browse_web,
        name="browse_web",
        description="Fetch and browse any web URL. Returns the HTML content, extracted text, and page title. Useful for accessing URLs returned from other tools or gathering web information.",
        args_schema=BrowseWebInput
    )
