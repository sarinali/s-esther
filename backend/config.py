import os
from typing import Optional

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


class Config:
    
    def __init__(self):
        self.APIFY_API_TOKEN: Optional[str] = os.getenv("APIFY_TOKEN")
        self.OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_KEY")
        self.GOOGLE_SEARCH_API_KEY: Optional[str] = os.getenv("GOOGLE_SEARCH_KEY")
        self.GOOGLE_SEARCH_ENGINE_ID: Optional[str] = os.getenv("GOOGLE_SEARCH_ENGINE_ID")
    def validate_required_config(self) -> None:
        """Validate that required configuration values are present."""
        required_configs = []
        if not self.APIFY_API_TOKEN:
            required_configs.append("APIFY_API_TOKEN")
        if not self.OPENAI_API_KEY:
            required_configs.append("OPENAI_KEY")
        if not self.GOOGLE_SEARCH_API_KEY:
            required_configs.append("GOOGLE_SEARCH_KEY")
        if not self.GOOGLE_SEARCH_ENGINE_ID:
            required_configs.append("GOOGLE_SEARCH_ENGINE_ID")

        if required_configs:
            raise ValueError(f"Required configuration values are missing: {required_configs}")

config = Config()

APIFY_API_TOKEN = config.APIFY_API_TOKEN
OPENAI_API_KEY = config.OPENAI_API_KEY
GOOGLE_SEARCH_API_KEY = config.GOOGLE_SEARCH_API_KEY
GOOGLE_SEARCH_ENGINE_ID = config.GOOGLE_SEARCH_ENGINE_ID