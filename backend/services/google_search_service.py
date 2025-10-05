from typing import List, Dict, Any, Optional

import requests

from config import config


class GoogleSearchService:
    def __init__(self):
        self.api_key = config.GOOGLE_SEARCH_API_KEY
        self.engine_id = config.GOOGLE_SEARCH_ENGINE_ID
        self.base_url = "https://www.googleapis.com/customsearch/v1"

    def search(
        self,
        query: str,
        num_results: int = 10
    ) -> Optional[Dict[str, Any]]:
        params = {
            "key": self.api_key,
            "cx": self.engine_id,
            "q": query,
            "num": min(num_results, 10)
        }

        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            if "items" not in data:
                return {"error": "No search results found", "query": query}

            results = []
            for item in data["items"]:
                results.append({
                    "title": item.get("title"),
                    "link": item.get("link"),
                    "snippet": item.get("snippet"),
                    "displayLink": item.get("displayLink")
                })

            return {
                "query": query,
                "totalResults": data.get("searchInformation", {}).get("totalResults"),
                "results": results
            }

        except requests.exceptions.RequestException as e:
            return {"error": f"Search request failed: {str(e)}", "query": query}
        except Exception as e:
            return {"error": f"Failed to process search results: {str(e)}", "query": query}


service = GoogleSearchService()
