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
    def validate_required_config(self) -> None:
        """Validate that required configuration values are present."""
        required_configs = []
        
        if not self.APIFY_API_TOKEN:
            required_configs.append("APIFY_API_TOKEN")


config = Config()

APIFY_API_TOKEN = config.APIFY_API_TOKEN
