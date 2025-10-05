from typing import Dict, Any, Optional

from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

from services.linkedin_service import service as linkedin_service


class LinkedInProfilePostsInput(BaseModel):
    profile_url: str = Field(description="The LinkedIn profile URL to fetch posts from")
    max_posts: int = Field(default=5, description="Maximum number of posts to retrieve (default: 5)")


def get_linkedin_profile_posts(profile_url: str, max_posts: int = 5) -> Optional[Dict[str, Any]]:
    posts_data = linkedin_service.get_profile_posts(profile_url, max_posts)

    if not posts_data:
        return {"error": "Failed to fetch LinkedIn profile posts", "profile_url": profile_url}

    return posts_data


def create_linkedin_profile_posts_tool() -> StructuredTool:
    return StructuredTool.from_function(
        func=get_linkedin_profile_posts,
        name="get_linkedin_profile_posts",
        description="Fetch recent posts from a LinkedIn profile URL. Returns post content, engagement metrics, and timestamps. Useful for evaluating prospect intent and activity. Default retrieves 10 posts.",
        args_schema=LinkedInProfilePostsInput
    )
