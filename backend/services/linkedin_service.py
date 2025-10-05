import re
from typing import List, Optional, Dict, Any

from services.apify_service import service as apify_service


class LinkedInService:
    def __init__(self):
        self.profile_detail_actor_id = "apimaestro/linkedin-profile-detail"
        self.profile_posts_actor_id = "apimaestro/linkedin-profile-posts"
        self.profile_reactions_actor_id = "apimaestro/linkedin-profile-reactions"
        self.company_posts_actor_id = "apimaestro/linkedin-company-posts"
        self.company_detail_actor_id = "apimaestro/linkedin-company-detail"

    def get_profile_details(
        self,
        profile_url: str
    ) -> Optional[Dict[str, Any]]:
        username_match = re.search(r'/(?:in|company)/([^/?]+?)(?:/|$|\?|#)', profile_url)
        username = username_match.group(1) if username_match else profile_url.split("/")[-1].rstrip('/')
        
        run_input = {
            "profileUrl": profile_url,
            "username": username
        }

        results = apify_service.run_actor_and_get_results(
            actor_id=self.profile_detail_actor_id,
            run_input=run_input,
            limit=1
        )

        if not results:
            return None

        return results[0]

    def get_profile_posts(
        self,
        profile_url: str,
        max_posts: int = 5
    ) -> Optional[List[Dict[str, Any]]]:
        username_match = re.search(r'/(?:in|company)/([^/?]+?)(?:/|$|\?|#)', profile_url)
        username = username_match.group(1) if username_match else profile_url.split("/")[-1].rstrip('/')

        run_input = {
            "profileUrl": profile_url,
            "username": username,
            "limit": max_posts
        }

        results = apify_service.run_actor_and_get_results(
            actor_id=self.profile_posts_actor_id,
            run_input=run_input,
            limit=max_posts
        )

        if not results:
            return None

        return results

    def get_profile_reactions(
        self,
        profile_url: str,
        max_reactions: int = 15
    ) -> Optional[List[Dict[str, Any]]]:
        username_match = re.search(r'/(?:in|company)/([^/?]+?)(?:/|$|\?|#)', profile_url)
        username = username_match.group(1) if username_match else profile_url.split("/")[-1].rstrip('/')

        run_input = {
            "profileUrl": profile_url,
            "username": username,
            "limit": max_reactions
        }

        results = apify_service.run_actor_and_get_results(
            actor_id=self.profile_reactions_actor_id,
            run_input=run_input,
            limit=max_reactions
        )

        if not results:
            return None

        return results

    def get_company_posts(
        self,
        company_url: str,
        max_posts: int = 6
    ) -> Optional[List[Dict[str, Any]]]:
        company_name_match = re.search(r'/company/([^/?]+?)(?:/|$|\?|#)', company_url)
        company_name = company_name_match.group(1) if company_name_match else company_url.split("/")[-1].rstrip('/')

        run_input = {
            "companyUrl": company_url,
            "companyName": company_name,
            "limit": max_posts
        }

        results = apify_service.run_actor_and_get_results(
            actor_id=self.company_posts_actor_id,
            run_input=run_input,
            limit=max_posts
        )

        if not results:
            return None

        return results

    def get_company_details(
        self,
        company_url: str
    ) -> Optional[Dict[str, Any]]:
        company_name_match = re.search(r'/company/([^/?]+?)(?:/|$|\?|#)', company_url)
        company_name = company_name_match.group(1) if company_name_match else company_url.split("/")[-1].rstrip('/')

        run_input = {
            "companyUrl": company_url,
            "companyName": company_name
        }

        results = apify_service.run_actor_and_get_results(
            actor_id=self.company_detail_actor_id,
            run_input=run_input,
            limit=1
        )

        if not results:
            return None

        return results[0]


service = LinkedInService()
