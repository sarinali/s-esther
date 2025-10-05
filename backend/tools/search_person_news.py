from typing import Dict, Any, Optional

from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

from services.google_search_service import service as google_search_service
from services.openai_service import service as openai_service


class SearchPersonNewsInput(BaseModel):
    person_name: str = Field(description="The person's name to search news for")
    person_context: str = Field(description="Context about the person (company, role, industry). Example: 'CEO of Sentra, cybersecurity' or 'CTO at Acme Corp'")
    num_results: int = Field(default=10, description="Number of results to return (max 10, default 10)")


def search_person_news(person_name: str, person_context: str, num_results: int = 10) -> Optional[Dict[str, Any]]:
    query_terms = [
        f'"{person_name}"',
        person_context,
        "(interview OR speaking OR appointment OR promoted OR joined OR announcement OR award OR keynote)"
    ]

    query = " ".join(query_terms)

    results = google_search_service.search(query, num_results)

    if not results or "error" in results:
        return {"error": "Failed to search person news", "person_name": person_name}

    validation_prompt = f"""You are validating search results for person news.

Target Person: {person_name}
Person Context: {person_context}

Search Results:
{results.get('results', [])}

Task: Filter out any results that are clearly about a DIFFERENT person with the same name. Return only the result indices (0-indexed) that are relevant to the target person.

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

    results["search_type"] = "person_news"
    results["person_name"] = person_name
    results["person_context"] = person_context

    return results


def create_search_person_news_tool() -> StructuredTool:
    return StructuredTool.from_function(
        func=search_person_news,
        name="search_person_news",
        description="Search for news mentions, interviews, speaking engagements, and announcements about a specific person. Validates their authority, influence, and thought leadership. Useful for BANT Authority assessment and finding external validation beyond LinkedIn. IMPORTANT: Always provide person_context (company, role, industry) to disambiguate from other people with the same name. The tool uses LLM validation to filter out irrelevant results.",
        args_schema=SearchPersonNewsInput
    )
