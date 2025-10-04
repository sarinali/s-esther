import re
from typing import List, Union

from constants.search_models import UserProfile
from services.linkedin_scraper_service import service as linkedin_service
from services.logger_service import logger_service


class QueryParseService:
    def __init__(self):
        self.linkedin_profile_pattern = re.compile(
            r"^https?://(?:www\.)?linkedin\.com/in/([a-zA-Z0-9\-]+)/?(?:\?.*)?$"
        )

    async def process_query(self, query: str) -> Union[UserProfile, List[UserProfile]]:
        query = query.strip()

        if self.is_linkedin_profile_url(query):
            logger_service.info(f"Detected LinkedIn profile URL: {query}")
            return await linkedin_service.get_single_profile(query)
        else:
            logger_service.info(f"Detected search query: {query}")
            return await linkedin_service.get_user_profiles(query)

    def is_linkedin_profile_url(self, query: str) -> bool:
        return bool(self.linkedin_profile_pattern.match(query))

    def extract_username_from_linkedin_url(self, url: str) -> str:
        match = self.linkedin_profile_pattern.match(url)
        if match:
            return match.group(1)
        return None


service = QueryParseService()