from typing import Dict, Any, Optional

from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

from services.linkedin_service import service as linkedin_service


class LinkedInCompanyPostsInput(BaseModel):
    company_url: str = Field(description="The LinkedIn company URL to fetch posts from")
    max_posts: int = Field(default=6, description="Maximum number of posts to retrieve (default: 6)")


def get_linkedin_company_posts(company_url: str, max_posts: int = 6) -> Optional[Dict[str, Any]]:
    posts_data = linkedin_service.get_company_posts(company_url, max_posts)

    if not posts_data:
        return {"error": "Failed to fetch LinkedIn company posts", "company_url": company_url}

    return posts_data


def create_linkedin_company_posts_tool() -> StructuredTool:
    return StructuredTool.from_function(
        func=get_linkedin_company_posts,
        name="get_linkedin_company_posts",
        description="Fetch recent posts from a LinkedIn company page URL. Returns post content, engagement metrics, and timestamps. Useful for understanding company messaging and activity. Default retrieves 15 posts.",
        args_schema=LinkedInCompanyPostsInput
    )
