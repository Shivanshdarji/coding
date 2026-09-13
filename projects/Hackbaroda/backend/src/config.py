import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / ".env"

load_dotenv(ENV_FILE, override=True)

APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN", "").strip()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip()
OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "output"))

# Apify actor IDs
TRENDING_ACTOR = "agentx/instagram-trending-scraper"
HASHTAG_ACTOR = "breathtaking_anthem/instagram-hashtag-posts-scraper"

SUPPORTED_COUNTRIES = [
    "United States", "Canada", "United Kingdom", "Australia",
    "Germany", "France", "Italy", "Spain", "Netherlands",
    "Brazil", "Mexico", "Japan", "South Korea", "India",
    "Indonesia", "United Arab Emirates", "Turkey",
]


def validate_token() -> str:
    if not APIFY_API_TOKEN:
        if not ENV_FILE.exists():
            raise ValueError(
                "No .env file found. Copy .env.example to .env and add your Apify token "
                "from https://console.apify.com/account/integrations"
            )
        if ENV_FILE.stat().st_size == 0:
            raise ValueError(
                ".env file is empty — save it in your editor (Ctrl+S) with: "
                "APIFY_API_TOKEN=your_token_here"
            )
        raise ValueError(
            "APIFY_API_TOKEN missing in .env. Add this line and save the file:\n"
            "APIFY_API_TOKEN=your_token_here"
        )
    return APIFY_API_TOKEN


def validate_openai_key() -> str:
    if not OPENAI_API_KEY:
        raise ValueError(
            "OPENAI_API_KEY not set. Add it to .env from "
            "https://platform.openai.com/api-keys"
        )
    return OPENAI_API_KEY
