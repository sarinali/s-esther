import os
from typing import Optional
from contextlib import contextmanager

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

from services.logger_service import logger_service


class BrowserService:
    def __init__(self):
        self._driver: Optional[webdriver.Chrome] = None
        self._is_logged_in = False
        self._linkedin_email = os.getenv("LINKEDIN_EMAIL", "donuts5.2022@gmail.com")
        self._linkedin_password = os.getenv("LINKEDIN_PASSWORD", "scrape123")

    def initialize(self):
        if self._driver is not None:
            logger_service.warning("Browser already initialized")
            return

        logger_service.info("Initializing Chrome browser")
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--headless")

        self._driver = webdriver.Chrome(options=chrome_options)
        logger_service.info("Chrome browser initialized successfully")

        self._perform_linkedin_login()

    def _perform_linkedin_login(self):
        if self._is_logged_in:
            return

        logger_service.info("Performing LinkedIn login")
        try:
            self._driver.get("https://www.linkedin.com/feed/")

            wait = WebDriverWait(self._driver, 10)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            username_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
            username_field.send_keys(self._linkedin_email)

            password_field = wait.until(EC.presence_of_element_located((By.ID, "password")))
            password_field.send_keys(self._linkedin_password)

            sign_in_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn__primary--large.from__button--floating")))
            sign_in_button.click()

            sleep(3)

            self._is_logged_in = True
            logger_service.info("LinkedIn login successful")

        except Exception as e:
            logger_service.error(f"LinkedIn login failed: {e}")
            raise

    @contextmanager
    def new_tab(self):
        if not self._driver:
            raise RuntimeError("Browser not initialized")

        original_handles = self._driver.window_handles
        self._driver.execute_script("window.open('');")
        new_handle = [h for h in self._driver.window_handles if h not in original_handles][0]

        try:
            self._driver.switch_to.window(new_handle)
            yield self._driver
        finally:
            try:
                self._driver.close()
                if self._driver.window_handles:
                    self._driver.switch_to.window(self._driver.window_handles[0])
            except Exception as e:
                logger_service.warning(f"Error closing tab: {e}")

    def shutdown(self):
        if self._driver:
            logger_service.info("Shutting down browser")
            try:
                self._driver.quit()
            except Exception as e:
                logger_service.error(f"Error during browser shutdown: {e}")
            finally:
                self._driver = None
                self._is_logged_in = False

    @property
    def is_initialized(self) -> bool:
        return self._driver is not None

    @property
    def is_logged_in(self) -> bool:
        return self._is_logged_in


service = BrowserService()