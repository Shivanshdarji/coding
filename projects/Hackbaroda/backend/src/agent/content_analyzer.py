"""Deep per-post/reel analysis using OpenAI."""

from pydantic import BaseModel, Field

from src.agent.openai_client import call_structured
from src.models.content import ContentItem
from src.models.strategy import PostDeepAnalysis

SYSTEM_PROMPT = """You are an elite Instagram content strategist and viral content analyst.
You reverse-engineer top-performing reels and posts to explain exactly how they were made,
why they went viral, and how creators can replicate the formula.

Be extremely specific and actionable. Reference real details from the scraped data.
For reels: analyze pacing, hook timing, visual cuts, text overlays, and audio choices.
For posts/carousels: analyze slide structure, visual hierarchy, and caption storytelling.
Never be generic. Every insight must tie back to the actual content provided."""


class PostAnalysisResponse(BaseModel):
    format_label: str
    how_it_was_made: str
    hook_analysis: str
    caption_breakdown: str
    visual_style: str
    audio_strategy: str = ""
    why_viral: list[str]
    engagement_insights: str
    replication_guide: list[str]
    key_takeaways: list[str]


def _build_post_prompt(item: ContentItem, rank: int) -> str:
    content_label = "Reel" if item.is_video else item.content_type.replace("_", " ").title()

    return f"""Analyze this trending Instagram {content_label} in full detail.

RANK: #{rank}
URL: {item.url}
CREATOR: @{item.username}
FORMAT: {content_label}
SECTION: {item.section or "Unknown"}
TOPIC: {item.topic or "Unknown"}
LIKES: {item.likes:,}
COMMENTS: {item.comments:,}
PLAYS/VIEWS: {item.plays:,}
VIRAL SCORE: {item.viral_score:,.0f}
DURATION: {item.duration or "N/A"} seconds
AUDIO: {item.audio_title or "N/A"}
HASHTAGS: {", ".join("#" + h for h in item.hashtags) or "None"}
PUBLISHED: {item.published_at or "Unknown"}

CAPTION:
{item.caption or "(no caption)"}

Provide a complete breakdown of how this content was likely produced, why it performs well,
what hook it uses, and how a creator can replicate this format successfully."""


def _call_analysis(item: ContentItem, rank: int, image_url: str | None):
    prompt = _build_post_prompt(item, rank)
    if not image_url:
        prompt += (
            "\n\nNote: Image preview unavailable (expired CDN link). "
            "Infer visual style from caption, format, topic, and engagement data."
        )
    return call_structured(
        SYSTEM_PROMPT,
        prompt,
        PostAnalysisResponse,
        image_url=image_url,
    )


def analyze_post(item: ContentItem, rank: int, *, use_vision: bool = True) -> PostDeepAnalysis:
    """Run deep OpenAI analysis on a single scraped post or reel."""
    image_url = None
    if use_vision and (item.thumbnail_url or item.image_url):
        image_url = item.thumbnail_url or item.image_url

    try:
        response = _call_analysis(item, rank, image_url)
    except Exception as e:
        # Instagram CDN URLs expire quickly — fall back to text-only analysis
        if image_url and "invalid_image_url" in str(e):
            response = _call_analysis(item, rank, None)
        else:
            raise

    content_label = "Reel" if item.is_video else item.content_type.replace("_", " ").title()

    return PostDeepAnalysis(
        rank=rank,
        url=item.url,
        username=item.username,
        content_type=item.content_type,
        format_label=response.format_label or content_label,
        how_it_was_made=response.how_it_was_made,
        hook_analysis=response.hook_analysis,
        caption_breakdown=response.caption_breakdown,
        visual_style=response.visual_style,
        audio_strategy=response.audio_strategy or None,
        why_viral=response.why_viral,
        engagement_insights=response.engagement_insights,
        replication_guide=response.replication_guide,
        key_takeaways=response.key_takeaways,
        scraped_data=item,
    )
