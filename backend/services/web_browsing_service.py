from typing import Optional, Dict, Any

import requests
from bs4 import BeautifulSoup


class WebBrowsingService:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.timeout = 10

    def fetch_url(self, url: str) -> Optional[Dict[str, Any]]:
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            for script in soup(["script", "style"]):
                script.decompose()

            text_content = soup.get_text(separator='\n', strip=True)

            return {
                "url": url,
                "status_code": response.status_code,
                "html": response.text,
                "text": text_content,
                "title": soup.title.string if soup.title else None
            }

        except requests.exceptions.Timeout:
            return {"error": "Request timed out", "url": url}
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}", "url": url}
        except Exception as e:
            return {"error": f"Failed to parse content: {str(e)}", "url": url}


service = WebBrowsingService()
