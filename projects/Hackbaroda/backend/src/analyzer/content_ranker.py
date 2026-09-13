"""Rank and score Instagram content by viral potential."""

from datetime import datetime, timezone

from src.models.content import ContentItem, ContentSuggestion


def _recency_multiplier(published_at: datetime | None) -> float:
    """Boost newer content — trending posts from last 7 days score higher."""
    if not published_at:
        return 1.0

    now = datetime.now(timezone.utc)
    if published_at.tzinfo is None:
        published_at = published_at.replace(tzinfo=timezone.utc)

    age_days = (now - published_at).days
    if age_days <= 1:
        return 1.5
    if age_days <= 3:
        return 1.3
    if age_days <= 7:
        return 1.15
    if age_days <= 30:
        return 1.0
    return 0.8


def calculate_viral_score(item: ContentItem) -> float:
    """
    Composite viral score weighing engagement signals.

    Weights: plays (views) matter most for reels, comments signal
    strong audience interaction, likes are baseline engagement.
    """
    likes = item.likes
    comments = item.comments
    plays = item.plays

    base_score = likes + (comments * 3) + (plays * 0.05)

    if item.is_video or item.content_type == "clips":
        base_score *= 1.2

    if item.is_verified:
        base_score *= 1.1

    if item.follower_count and item.follower_count > 0:
        engagement_rate = (likes + comments) / item.follower_count
        item.engagement_rate = round(engagement_rate * 100, 2)
        if engagement_rate > 0.05:
            base_score *= 1.3
        elif engagement_rate > 0.02:
            base_score *= 1.15

    base_score *= _recency_multiplier(item.published_at)

    return round(base_score, 2)


def rank_content(items: list[ContentItem]) -> list[ContentItem]:
    """Score and sort content by viral potential (highest first)."""
    for item in items:
        item.viral_score = calculate_viral_score(item)
    return sorted(items, key=lambda x: x.viral_score, reverse=True)


def _build_why_trending(item: ContentItem) -> str:
    parts = []

    if item.plays > 100_000:
        parts.append(f"{item.plays:,} views")
    elif item.plays > 10_000:
        parts.append(f"{item.plays:,} plays")

    if item.likes > 50_000:
        parts.append(f"{item.likes:,} likes")
    elif item.likes > 5_000:
        parts.append(f"{item.likes:,} likes")

    if item.comments > 1_000:
        parts.append(f"{item.comments:,} comments")

    if item.section:
        parts.append(f"trending in {item.section}")
    if item.topic:
        parts.append(f"topic: {item.topic}")

    if item.is_video:
        parts.append("reel/video format")

    if item.engagement_rate > 5:
        parts.append(f"{item.engagement_rate}% engagement rate")

    if not parts:
        parts.append("high engagement signals")

    return " | ".join(parts)


def _generate_content_ideas(item: ContentItem) -> list[str]:
    """Suggest content ideas inspired by a top-performing post."""
    ideas = []

    if item.is_video or item.content_type == "clips":
        ideas.append("Create a reel in a similar format — reels dominate Explore")
    else:
        ideas.append("Try a carousel post — multi-slide content gets high saves")

    if item.topic:
        ideas.append(f"Cover the '{item.topic}' niche — it's trending on Explore")
    elif item.hashtag:
        ideas.append(f"Use #{item.hashtag} — top posts are performing well")

    if item.audio_title:
        ideas.append(f"Use trending audio: '{item.audio_title}'")

    if item.caption and len(item.caption) > 100:
        ideas.append("Write detailed captions — top posts use storytelling hooks")
    else:
        ideas.append("Keep captions punchy with a strong hook in the first line")

    if item.hashtags:
        top_tags = item.hashtags[:5]
        ideas.append(f"Try these hashtags: {' '.join('#' + t for t in top_tags)}")

    return ideas[:4]


def generate_suggestions(
    items: list[ContentItem],
    top_n: int = 10,
) -> list[ContentSuggestion]:
    """Rank content and produce actionable suggestions."""
    ranked = rank_content(items)

    suggestions = []
    for i, item in enumerate(ranked[:top_n], start=1):
        suggestions.append(
            ContentSuggestion(
                rank=i,
                item=item,
                why_trending=_build_why_trending(item),
                content_ideas=_generate_content_ideas(item),
            )
        )

    return suggestions
