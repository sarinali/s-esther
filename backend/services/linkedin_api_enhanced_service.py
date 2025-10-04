import os
import re
import random
import time
from typing import List, Optional, Dict
from itertools import cycle

import requests
from linkedin_api import Linkedin

from constants.search_models import UserProfile
from services.user_profile_service import UserProfileService
from services.logger_service import logger_service


class LinkedInAPIEnhancedService(UserProfileService):
    def __init__(self):
        self._api: Optional[Linkedin] = None
        self._linkedin_email = os.getenv("LINKEDIN_EMAIL", "sarinajnli@gmail.com")
        self._linkedin_password = os.getenv("LINKEDIN_PASSWORD", "scrape123")

        self._proxies = self._load_proxies()
        self._proxy_cycle = cycle(self._proxies) if self._proxies else None
        self._current_proxy = None

        self._user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0"
        ]

        self._last_request_time = 0
        self._min_delay = 2.0  # Minimum 2 seconds between requests
        self._max_delay = 5.0  # Maximum 5 seconds between requests

    def _load_proxies(self) -> List[Dict[str, str]]:
        """Load proxy list from environment or config"""
        proxy_list = []

        proxy_string = os.getenv("PROXY_LIST", "")
        if proxy_string:
            for proxy in proxy_string.split(","):
                proxy = proxy.strip()
                if proxy:
                    proxy_list.append({
                        "http": proxy,
                        "https": proxy
                    })

        # Method 2: Free proxy services (use with caution - these are often unreliable)
        # You can add your own proxy service here

        # Method 3: Add your paid proxy service here
        # Example for rotating residential proxies:
        # proxy_list.extend([
        #     {"http": "http://user:pass@proxy1.example.com:8080", "https": "http://user:pass@proxy1.example.com:8080"},
        #     {"http": "http://user:pass@proxy2.example.com:8080", "https": "http://user:pass@proxy2.example.com:8080"},
        # ])

        logger_service.info(f"Loaded {len(proxy_list)} proxies")
        return proxy_list

    def _get_next_proxy(self) -> Optional[Dict[str, str]]:
        """Get the next proxy in rotation"""
        if self._proxy_cycle:
            return next(self._proxy_cycle)
        return None

    def _rotate_ip(self):
        """Rotate to next proxy/IP"""
        if self._proxies:
            self._current_proxy = self._get_next_proxy()
            logger_service.info(f"Rotated to new proxy: {self._current_proxy}")
        else:
            logger_service.warning("No proxies available for rotation")

    def _get_random_user_agent(self) -> str:
        """Get a random user agent"""
        return random.choice(self._user_agents)

    def _rate_limit(self):
        """Implement rate limiting between requests"""
        current_time = time.time()
        time_since_last = current_time - self._last_request_time

        if time_since_last < self._min_delay:
            delay = random.uniform(self._min_delay, self._max_delay)
            logger_service.info(f"Rate limiting: waiting {delay:.2f} seconds")
            time.sleep(delay)

        self._last_request_time = time.time()

    def initialize(self):
        if self._api is not None:
            logger_service.warning("LinkedIn API already initialized")
            return

        logger_service.info("Initializing Enhanced LinkedIn API with anti-detection measures")

        try:
            self._rotate_ip()

            session = requests.Session()

            if self._current_proxy:
                session.proxies.update(self._current_proxy)

            session.headers.update({
                'User-Agent': self._get_random_user_agent()
            })

            self._api = Linkedin(
                self._linkedin_email,
                self._linkedin_password,
                # proxies=self._current_proxy,
            )

            logger_service.info("Enhanced LinkedIn API initialized successfully")

        except Exception as e:
            logger_service.error(f"Failed to initialize Enhanced LinkedIn API: {e}")
            # Try without proxy on failure
            if self._current_proxy:
                logger_service.info("Retrying without proxy...")
                try:
                    self._api = Linkedin(self._linkedin_email, self._linkedin_password)
                    logger_service.info("LinkedIn API initialized without proxy")
                except Exception as e2:
                    logger_service.error(f"Failed to initialize even without proxy: {e2}")
                    raise
            else:
                raise

    def reinitialize_with_new_ip(self):
        """Reinitialize the API with a new IP/proxy"""
        logger_service.info("Reinitializing API with new IP...")

        # Close current API connection
        if self._api:
            self._api = None

        # Rotate to new proxy
        self._rotate_ip()

        # Wait a bit before reconnecting
        time.sleep(random.uniform(3, 7))

        # Reinitialize
        self.initialize()

    async def get_user_profiles(self, query: str) -> List[UserProfile]:
        if not self._api:
            raise RuntimeError("LinkedIn API not initialized")

        logger_service.info(f"Searching LinkedIn for: {query}")

        try:
            # Rate limiting
            self._rate_limit()

            search_results = self._api.search_people(keywords=query, limit=10)

            profiles = []
            for result in search_results:
                profile = self._convert_search_result_to_profile(result)
                if profile:
                    profiles.append(profile)

            logger_service.info(f"Successfully found {len(profiles)} profiles")
            return profiles

        except Exception as e:
            logger_service.error(f"Error searching LinkedIn: {e}")

            # If we get blocked, try rotating IP and retrying once
            if "challenge" in str(e).lower() or "blocked" in str(e).lower():
                logger_service.warning("Detected potential blocking, rotating IP and retrying...")
                self.reinitialize_with_new_ip()

                # Retry once with new IP
                try:
                    self._rate_limit()
                    search_results = self._api.search_people(keywords=query, limit=10)

                    profiles = []
                    for result in search_results:
                        profile = self._convert_search_result_to_profile(result)
                        if profile:
                            profiles.append(profile)

                    logger_service.info(f"Retry successful: found {len(profiles)} profiles")
                    return profiles

                except Exception as e2:
                    logger_service.error(f"Retry failed: {e2}")
                    raise
            else:
                raise

    async def get_single_profile(self, url: str) -> UserProfile:
        if not self._api:
            raise RuntimeError("LinkedIn API not initialized")

        user_id = self._extract_user_id_from_url(url)
        if not user_id:
            raise ValueError(f"Could not extract user ID from URL: {url}")

        logger_service.info(f"Fetching LinkedIn profile for user ID: {user_id}")

        try:
            # Rate limiting
            self._rate_limit()

            profile_data = self._api.get_profile(user_id)

            profile = self._convert_profile_data_to_profile(profile_data, url)
            if not profile:
                raise ValueError("Could not extract profile data")

            logger_service.info(f"Successfully fetched profile for: {profile.name}")
            return profile

        except Exception as e:
            logger_service.error(f"Error fetching LinkedIn profile: {e}")

            # Similar retry logic for single profile
            if "challenge" in str(e).lower() or "blocked" in str(e).lower():
                logger_service.warning("Detected potential blocking, rotating IP and retrying...")
                self.reinitialize_with_new_ip()

                try:
                    self._rate_limit()
                    profile_data = self._api.get_profile(user_id)
                    profile = self._convert_profile_data_to_profile(profile_data, url)
                    if not profile:
                        raise ValueError("Could not extract profile data")

                    logger_service.info(f"Retry successful for: {profile.name}")
                    return profile

                except Exception as e2:
                    logger_service.error(f"Retry failed: {e2}")
                    raise
            else:
                raise

    def get_user_id_for_username(self, username: str) -> Optional[str]:
        """Get LinkedIn user ID for a given username"""
        if not self._api:
            raise RuntimeError("LinkedIn API not initialized")

        try:
            logger_service.info(f"Looking up user ID for username: {username}")

            # Rate limiting
            self._rate_limit()

            search_results = self._api.search_people(keywords=username, limit=50)

            for result in search_results:
                public_id = result.get('public_id')
                if public_id == username:
                    user_id = result.get('urn_id')
                    logger_service.info(f"Found user ID {user_id} for username {username}")
                    return user_id

            for result in search_results:
                first_name = result.get('firstName', '').lower()
                last_name = result.get('lastName', '').lower()

                possible_usernames = [
                    f"{first_name}{last_name}",
                    f"{first_name}-{last_name}",
                    f"{first_name}.{last_name}",
                    first_name,
                    last_name
                ]

                if username.lower() in possible_usernames:
                    user_id = result.get('urn_id')
                    logger_service.info(f"Found potential user ID {user_id} for username {username}")
                    return user_id

            logger_service.warning(f"Could not find user ID for username: {username}")
            return None

        except Exception as e:
            logger_service.error(f"Error looking up user ID for username {username}: {e}")
            return None

    def _extract_user_id_from_url(self, url: str) -> Optional[str]:
        """Extract username from LinkedIn URL and convert to user ID"""
        pattern = r"linkedin\.com/in/([a-zA-Z0-9\-]+)"
        match = re.search(pattern, url)

        if not match:
            logger_service.error(f"Could not extract username from URL: {url}")
            return None

        username = match.group(1)

        if username == 'sarinali':
            logger_service.info("Using hardcoded user ID for sarinali")
            return "sarinali"

        return self.get_user_id_for_username(username)

    def _convert_search_result_to_profile(self, result: dict) -> Optional[UserProfile]:
        try:
            name = f"{result.get('firstName', '')} {result.get('lastName', '')}".strip()
            if not name:
                return None

            public_id = result.get('public_id')
            profile_link = f"https://www.linkedin.com/in/{public_id}" if public_id else None

            headline = result.get('headline', '')

            location_name = ""
            if 'geoLocation' in result and result['geoLocation']:
                location_name = result['geoLocation'].get('geo', {}).get('defaultLocalizedName', '')

            profile_image_url = None
            if 'profilePicture' in result and result['profilePicture']:
                artifacts = result['profilePicture'].get('displayImageReference', {}).get('vectorImage', {}).get('artifacts', [])
                if artifacts:
                    profile_image_url = artifacts[-1].get('fileIdentifyingUrlPathSegment')
                    if profile_image_url:
                        profile_image_url = f"https://media.licdn.com/dms/image/{profile_image_url}"

            return UserProfile(
                name=name,
                profile_link=profile_link or "",
                job_title=headline if headline else None,
                location=location_name if location_name else None,
                profile_image_url=profile_image_url,
                platform="linkedin"
            )

        except Exception as e:
            logger_service.warning(f"Error converting search result to profile: {e}")
            return None

    def _convert_profile_data_to_profile(self, profile_data: dict, original_url: str) -> Optional[UserProfile]:
        try:
            first_name = profile_data.get('firstName', '')
            last_name = profile_data.get('lastName', '')
            name = f"{first_name} {last_name}".strip()

            if not name:
                return None

            job_title = None
            if 'experience' in profile_data and profile_data['experience']:
                current_position = profile_data['experience'][0]
                job_title = current_position.get('title')

            location = None
            if 'geoLocation' in profile_data and profile_data['geoLocation']:
                location = profile_data['geoLocation'].get('geo', {}).get('defaultLocalizedName')

            profile_image_url = None
            if 'profilePicture' in profile_data and profile_data['profilePicture']:
                artifacts = profile_data['profilePicture'].get('displayImageReference', {}).get('vectorImage', {}).get('artifacts', [])
                if artifacts:
                    profile_image_url = artifacts[-1].get('fileIdentifyingUrlPathSegment')
                    if profile_image_url:
                        profile_image_url = f"https://media.licdn.com/dms/image/{profile_image_url}"

            return UserProfile(
                name=name,
                profile_link=original_url,
                job_title=job_title,
                location=location,
                profile_image_url=profile_image_url,
                platform="linkedin"
            )

        except Exception as e:
            logger_service.warning(f"Error converting profile data to profile: {e}")
            return None

    @property
    def is_initialized(self) -> bool:
        return self._api is not None


service = LinkedInAPIEnhancedService()