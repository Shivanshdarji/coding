"""Scrape Instagram Explore / trending feed via Apify."""

from datetime import datetime
from typing import Optional

from apify_client import ApifyClient

from src.config import TRENDING_ACTOR, validate_token
from src.models.content import ContentItem
from src.scrapers.apify_utils import get_dataset_id


def _parse_timestamp(value) -> Optional[datetime]:
    if not value:
        return None
    if isinstance(value, int):
        return datetime.fromtimestamp(value)
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except (ValueError, TypeError):
        return None


def _extract_hashtags(caption: str) -> list[str]:
    return [tag.lstrip("#") for tag in caption.split() if tag.startswith("#")]


def _normalize_trending_item(raw: dict) -> ContentItem:
    caption = raw.get("caption") or ""
    return ContentItem(
        id=str(raw.get("id", raw.get("code", ""))),
        url=raw.get("url", f"https://www.instagram.com/p/{raw.get('code', '')}/"),
        username=raw.get("username", "unknown"),
        caption=caption,
        likes=int(raw.get("likes") or 0),
        comments=int(raw.get("comments") or 0),
        plays=int(raw.get("plays") or 0),
        is_video=bool(raw.get("is_video")),
        content_type=raw.get("type", "feed"),
        section=raw.get("section"),
        topic=raw.get("topic"),
        hashtags=_extract_hashtags(caption),
        image_url=raw.get("image_url"),
        video_url=raw.get("video_url"),
        thumbnail_url=raw.get("thumbnail_url"),
        duration=raw.get("duration"),
        published_at=_parse_timestamp(raw.get("date") or raw.get("timestamp")),
        source="trending",
    )


def scrape_trending(
    max_results: int = 50,
    country: str = "United States",
    download_medias: str = "none",
) -> list[ContentItem]:
    """
    Scrape Instagram Explore trending content.

    Uses Apify's Instagram Trending Scraper to pull posts from
    Instagram's Explore feed with engagement metrics and topic labels.
    """
    token = validate_token()
    client = ApifyClient(token)

    run_input = {
        "max_results": max(max_results, 10),
        "download_medias": download_medias,
        "country": country,
    }

    print(f"Scraping {max_results} trending posts from Instagram Explore ({country})...")
    run = client.actor(TRENDING_ACTOR).call(run_input=run_input)

    items = []
    for raw in client.dataset(get_dataset_id(run)).iterate_items():
        items.append(_normalize_trending_item(raw))

    print(f"Scraped {len(items)} trending posts.")
    return items
