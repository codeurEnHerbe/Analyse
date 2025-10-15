import os
from dataclasses import dataclass

try:
    from dotenv import load_dotenv
except Exception:
    def load_dotenv(path: str = ".env"):
        if not os.path.exists(path):
            return
        for line in open(path, "r", encoding="utf-8"):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

load_dotenv()

@dataclass
class Settings:
    api_key: str
    platform_region: str = "euw1"
    regional_routing: str = "europe"
    default_count: int = 10
    log_level: str = "DEBUG"


def load_settings() -> Settings:
    ak = os.getenv("RIOT_API_KEY")
    if not ak:
        raise RuntimeError("missing RIOT_API_KEY")
    # Seule l'API key est dans .env, le reste est configuré via CLI
    pr = os.getenv("PLATFORM_REGION", "euw1")
    rr = os.getenv("REGIONAL_ROUTING", "europe")
    dc = int(os.getenv("DEFAULT_COUNT", "10"))
    ll = os.getenv("LOG_LEVEL", "DEBUG")
    return Settings(api_key=ak, platform_region=pr, regional_routing=rr, default_count=dc, log_level=ll)
