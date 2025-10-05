from typing import Dict, Any, Optional

from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

from services.linkedin_service import service as linkedin_service


class LinkedInCompanyDetailsInput(BaseModel):
    company_url: str = Field(description="The LinkedIn company URL to fetch details from")


def get_linkedin_company_details(company_url: str) -> Optional[Dict[str, Any]]:
    company_data = linkedin_service.get_company_details(company_url)

    if not company_data:
        return {"error": "Failed to fetch LinkedIn company details", "company_url": company_url}

    return company_data


def create_linkedin_company_details_tool() -> StructuredTool:
    return StructuredTool.from_function(
        func=get_linkedin_company_details,
        name="get_linkedin_company_details",
        description="Fetch detailed information from a LinkedIn company page URL. Returns comprehensive company data including description, employee count, industry, location, and more.",
        args_schema=LinkedInCompanyDetailsInput
    )
