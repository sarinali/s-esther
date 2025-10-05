from typing import Dict, Any, Optional

from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

from services.linkedin_service import service as linkedin_service


class LinkedInProfileReactionsInput(BaseModel):
    profile_url: str = Field(description="The LinkedIn profile URL to fetch reactions from")
    max_reactions: int = Field(default=15, description="Maximum number of reactions to retrieve (default: 15)")


def get_linkedin_profile_reactions(profile_url: str, max_reactions: int = 15) -> Optional[Dict[str, Any]]:
    reactions_data = linkedin_service.get_profile_reactions(profile_url, max_reactions)

    if not reactions_data:
        return {"error": "Failed to fetch LinkedIn profile reactions", "profile_url": profile_url}

    return reactions_data


def create_linkedin_profile_reactions_tool() -> StructuredTool:
    return StructuredTool.from_function(
        func=get_linkedin_profile_reactions,
        name="get_linkedin_profile_reactions",
        description="Fetch recent reactions/engagement from a LinkedIn profile URL. Shows what posts the person has reacted to, revealing their interests and intent signals. Default retrieves 15 reactions.",
        args_schema=LinkedInProfileReactionsInput
    )
