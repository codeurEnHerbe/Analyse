import time
import logging
import requests
from typing import Any, Dict, Optional
from . import RiotError

class RiotClient:
    def __init__(self, api_key: str, platform_region: str, regional_routing: str, user_agent: str = "riot-docfirst-kit/1.0", timeout: int = 15):
        self.api_key = api_key
        self.platform_region = platform_region
        self.regional_routing = regional_routing
        self.timeout = timeout
        self.s = requests.Session()
        self.s.headers.update({"User-Agent": user_agent, "X-Riot-Token": api_key})
        self.log = logging.getLogger("riot")

    def _get(self, url: str, params: Optional[Dict[str, Any]] = None, retry: int = 3) -> Dict[str, Any]:
        for i in range(retry):
            r = self.s.get(url, params=params, timeout=self.timeout)
            if r.status_code == 429:
                ra = r.headers.get("Retry-After")
                w = int(ra) if ra and ra.isdigit() else (2 ** i)
                self.log.warning("429 wait=%s attempt=%s url=%s", w, i + 1, url)
                time.sleep(w)
                continue
            if 200 <= r.status_code < 300:
                return r.json() if r.text else {}
            if 400 <= r.status_code < 500:
                raise RiotError(f"client {r.status_code} {r.text[:300]}")
            self.log.warning("server status=%s attempt=%s", r.status_code, i + 1)
            time.sleep(1 + 2 * i)
        raise RiotError("max retries")

    def platform_url(self, path: str) -> str:
        return f"https://{self.platform_region}.api.riotgames.com{path}"

    def regional_url(self, path: str) -> str:
        return f"https://{self.regional_routing}.api.riotgames.com{path}"
