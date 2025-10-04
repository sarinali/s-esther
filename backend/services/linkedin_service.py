import re
from typing import List, Optional, Dict, Any, Union

from constants.search_models import SearchUserPayload, UserProfile
from services.apify_service import service as apify_service


class LinkedInService:
    def __init__(self):
        self.profile_detail_actor_id = "apimaestro/linkedin-profile-detail"


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

    def _parse_profile_search_results(
        self,
        results: List[dict]
    ) -> List[UserProfile]:
        profiles = []

        for result in results:
            profile = UserProfile(
                name=result.get("name", ""),
                profile_link=result.get("profileUrl", ""),
                job_title=result.get("headline"),
                location=result.get("location"),
                profile_image_url=result.get("photoUrl"),
                platform="linkedin"
            )
            profiles.append(profile)

        return profiles


service = LinkedInService()
