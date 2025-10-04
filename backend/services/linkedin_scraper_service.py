from typing import List
from urllib.parse import quote

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from time import sleep

from constants.search_models import UserProfile
from services.user_profile_service import UserProfileService
from services.browser_service import service as browser_service
from services.logger_service import logger_service


class LinkedInScraperService(UserProfileService):
    def __init__(self):
        self.search_timeout = 15

    async def get_user_profiles(self, query: str) -> List[UserProfile]:
        if not browser_service.is_initialized:
            raise RuntimeError("Browser service not initialized")

        if not browser_service.is_logged_in:
            raise RuntimeError("Not logged into LinkedIn")

        logger_service.info(f"Searching LinkedIn for: {query}")

        try:
            with browser_service.new_tab() as driver:
                encoded_query = quote(query)
                search_url = f"https://www.linkedin.com/search/results/people/?keywords={encoded_query}&origin=CLUSTER_EXPANSION"

                driver.get(search_url)

                wait = WebDriverWait(driver, self.search_timeout)
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

                sleep(3)

                profiles = []
                try:
                    result_lis = driver.find_elements(By.CSS_SELECTOR, "li.vdwXPaZqjnOSVBOJRaUGXoYwopOhpiBiuQ")
                    logger_service.info(f"Found {len(result_lis)} LinkedIn profile results")

                    for li in result_lis:
                        profile = self._extract_profile_data(li)
                        if profile:
                            profiles.append(profile)

                except TimeoutException:
                    logger_service.warning(f"Timeout occurred while searching for: {query}")
                except Exception as e:
                    logger_service.error(f"Error extracting profiles: {e}")

                logger_service.info(f"Successfully extracted {len(profiles)} profiles")
                return profiles

        except WebDriverException as e:
            logger_service.error(f"WebDriver error during LinkedIn search: {e}")
            raise
        except Exception as e:
            logger_service.error(f"Unexpected error during LinkedIn search: {e}")
            raise

    async def get_single_profile(self, url: str) -> UserProfile:
        if not browser_service.is_initialized:
            raise RuntimeError("Browser service not initialized")

        if not browser_service.is_logged_in:
            raise RuntimeError("Not logged into LinkedIn")

        logger_service.info(f"Fetching single LinkedIn profile: {url}")

        try:
            with browser_service.new_tab() as driver:
                driver.get(url)

                wait = WebDriverWait(driver, self.search_timeout)
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

                sleep(3)

                try:
                    name = browser_service.safe_extract_text_from_driver(
                        driver,
                        "h1.text-heading-xlarge"
                    )

                    job_title = browser_service.safe_extract_text_from_driver(
                        driver,
                        ".text-body-medium.break-words"
                    )

                    location = browser_service.safe_extract_text_from_driver(
                        driver,
                        ".text-body-small.inline.t-black--light.break-words"
                    )

                    profile_image_url = browser_service.safe_extract_attribute_from_driver(
                        driver,
                        "img.pv-top-card-profile-picture__image",
                        "src"
                    )

                    if not name:
                        raise ValueError("Could not extract name from profile page")

                    profile = UserProfile(
                        name=name,
                        profile_link=url,
                        job_title=job_title,
                        location=location,
                        profile_image_url=profile_image_url,
                        platform="linkedin"
                    )

                    logger_service.info(f"Successfully extracted profile for: {name}")
                    return profile

                except Exception as e:
                    logger_service.error(f"Error extracting single profile data: {e}")
                    raise

        except WebDriverException as e:
            logger_service.error(f"WebDriver error during single profile fetch: {e}")
            raise
        except Exception as e:
            logger_service.error(f"Unexpected error during single profile fetch: {e}")
            raise

    def _extract_profile_data(self, li_element) -> UserProfile:
        try:
            name = browser_service.safe_extract_text(
                li_element,
                "a[data-test-app-aware-link] span[dir='ltr'] span[aria-hidden='true']"
            )

            profile_link = browser_service.safe_extract_attribute(
                li_element,
                "a[data-test-app-aware-link]",
                "href"
            )

            job_title = browser_service.safe_extract_text(
                li_element,
                "div.xRJOgrQuFzciyRxKOIOwvaYwLREkZzCCxtQk"
            )

            location = browser_service.safe_extract_text(
                li_element,
                "div.JcoRZcgVWQelOtLJFmykrzjWASePpwDbmoyVM"
            )

            profile_image_url = browser_service.safe_extract_attribute(
                li_element,
                "img.presence-entity__image",
                "src"
            )

            if not name or not profile_link:
                logger_service.warning("Skipping profile - missing required fields (name or profile_link)")
                return None

            return UserProfile(
                name=name,
                profile_link=profile_link,
                job_title=job_title,
                location=location,
                profile_image_url=profile_image_url,
                platform="linkedin"
            )

        except Exception as e:
            logger_service.warning(f"Error extracting profile data: {e}")
            return None


service = LinkedInScraperService()