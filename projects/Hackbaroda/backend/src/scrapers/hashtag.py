"""Scrape top-performing Instagram hashtag posts via Apify."""

from datetime import datetime
from typing import Optional

from apify_client import ApifyClient

from src.config import HASHTAG_ACTOR, validate_token
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


def _normalize_hashtag_item(raw: dict, hashtag: str) -> ContentItem:
    author = raw.get("author") or {}
    audio = raw.get("audio") or {}

    product_type = raw.get("product_type", "feed")
    is_video = product_type == "clips" or raw.get("media_type") == 2

    return ContentItem(
        id=str(raw.get("id", raw.get("shortcode", ""))),
        url=raw.get("url", f"https://www.instagram.com/p/{raw.get('shortcode', '')}/"),
        username=author.get("username", "unknown"),
        caption=raw.get("caption") or "",
        likes=int(raw.get("like_count") or 0),
        comments=int(raw.get("comment_count") or 0),
        plays=int(raw.get("play_count") or raw.get("ig_play_count") or 0),
        is_video=is_video,
        content_type=product_type,
        hashtags=raw.get("hashtags") or [],
        image_url=raw.get("thumbnail_url"),
        video_url=raw.get("video_url"),
        thumbnail_url=raw.get("thumbnail_url"),
        duration=int(raw.get("duration_seconds") or 0) or None,
        published_at=_parse_timestamp(
            raw.get("taken_at_timestamp") or raw.get("taken_at")
        ),
        source="hashtag",
        hashtag=hashtag,
        is_verified=bool(author.get("is_verified")),
        follower_count=author.get("follower_count"),
        audio_title=audio.get("title") or audio.get("original_audio_title"),
    )


def scrape_hashtag(
    hashtag: str,
    scrape_type: str = "top",
    max_items: int = 50,
) -> list[ContentItem]:
    """
    Scrape top or recent posts from an Instagram hashtag.

    scrape_type: 'top' for best-performing, 'recent' for latest posts.
    """
    token = validate_token()
    client = ApifyClient(token)

    clean_tag = hashtag.lstrip("#").strip()
    run_input = {
        "hashtag": clean_tag,
        "scrape_type": scrape_type,
        "max_items": max(max_items, 24),
    }

    print(f"Scraping #{clean_tag} ({scrape_type}) — up to {max_items} posts...")
    run = client.actor(HASHTAG_ACTOR).call(run_input=run_input)

    items = []
    for raw in client.dataset(get_dataset_id(run)).iterate_items():
        items.append(_normalize_hashtag_item(raw, clean_tag))

    print(f"Scraped {len(items)} posts from #{clean_tag}.")
    return items
