import httpx
import os
from dotenv import load_dotenv

load_dotenv()

class CanvasClient:
    def __init__(self):
        self.base_url = os.getenv("CANVAS_BASE_URL", "").rstrip("/")
        self.token = os.getenv("CANVAS_API_TOKEN", "")
        self.headers = {"Authorization": f"Bearer {self.token}"}

    def _get(self, endpoint: str, params: dict = None) -> list | dict:
        """Make a paginated GET request to the Canvas API."""
        url = f"{self.base_url}/api/v1/{endpoint}"
        results = []
        params = params or {}
        params["per_page"] = 100

        while url:
            response = httpx.get(url, headers=self.headers, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()

            if isinstance(data, list):
                results.extend(data)
            else:
                return data  # Single object response

            # Handle pagination
            url = None
            params = {}
            link_header = response.headers.get("Link", "")
            for part in link_header.split(","):
                if 'rel="next"' in part:
                    url = part.split(";")[0].strip().strip("<>")
                    break

        return results
