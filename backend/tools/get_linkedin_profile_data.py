from typing import Dict, Any, Optional

from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

from services.linkedin_service import service as linkedin_service


class LinkedInProfileInput(BaseModel):
    profile_url: str = Field(description="The LinkedIn profile URL to fetch data from")


def get_linkedin_profile_data(profile_url: str) -> Optional[Dict[str, Any]]:
    profile_data = linkedin_service.get_profile_details(profile_url)

    if not profile_data:
        return {"error": "Failed to fetch LinkedIn profile data", "profile_url": profile_url}

    return profile_data


def create_linkedin_profile_tool() -> StructuredTool:
    return StructuredTool.from_function(
        func=get_linkedin_profile_data,
        name="get_linkedin_profile_data",
        description="Fetch detailed profile information from a LinkedIn profile URL. Returns comprehensive profile data including work experience, education, skills, and more.",
        args_schema=LinkedInProfileInput
    )
