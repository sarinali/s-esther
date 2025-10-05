from typing import Dict, Any, Optional
from datetime import datetime, timedelta

from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

from services.google_search_service import service as google_search_service
from services.openai_service import service as openai_service


class SearchCompanyNewsInput(BaseModel):
    company_name: str = Field(description="The company name to search news for")
    company_context: str = Field(description="Brief context about the company (industry, website, or key details to disambiguate). Example: 'cybersecurity company, sentra.io' or 'automotive manufacturer'")
    timeframe_months: int = Field(default=6, description="How many months back to search (default: 6)")
    num_results: int = Field(default=10, description="Number of results to return (max 10, default 10)")


def search_company_news(company_name: str, company_context: str, timeframe_months: int = 6, num_results: int = 10) -> Optional[Dict[str, Any]]:
    query_terms = [
        f'"{company_name}"',
        company_context,
        "(funding OR acquisition OR partnership OR announcement OR funding OR investment OR growth OR expansion)"
    ]

    query = " ".join(query_terms)

    results = google_search_service.search(query, num_results)

    if not results or "error" in results:
        return {"error": "Failed to search company news", "company_name": company_name}

    validation_prompt = f"""You are validating search results for company news.

Target Company: {company_name}
Company Context: {company_context}

Search Results:
{results.get('results', [])}

Task: Filter out any results that are clearly about a DIFFERENT company with the same name. Return only the result indices (0-indexed) that are relevant to the target company.

Return your response as a JSON array of indices, like: [0, 1, 4]
If no results are relevant, return: []
If you're unsure about a result, include it (better to be inclusive)."""

    try:
        validation_response = openai_service.analyze_with_reasoning(
            prompt=validation_prompt,
            context=""
        )

        import json
        relevant_indices = json.loads(validation_response.strip())

        filtered_results = [results['results'][i] for i in relevant_indices if i < len(results['results'])]

        results['results'] = filtered_results
        results['original_count'] = len(results.get('results', []))
        results['filtered_count'] = len(filtered_results)

    except Exception as e:
        results['validation_error'] = f"Could not validate results: {str(e)}"

    results["search_type"] = "company_news"
    results["company_name"] = company_name
    results["company_context"] = company_context
    results["timeframe_months"] = timeframe_months

    return results


def create_search_company_news_tool() -> StructuredTool:
    return StructuredTool.from_function(
        func=search_company_news,
        name="search_company_news",
        description="Search for recent news and announcements about a specific company. Finds funding rounds, acquisitions, partnerships, expansions, and other newsworthy events. Essential for BANT Budget and Timing assessment. IMPORTANT: Always provide company_context (industry, website domain, or key details) to ensure accurate results and avoid confusion with other companies with the same name. The tool uses LLM validation to filter out irrelevant results.",
        args_schema=SearchCompanyNewsInput
    )
