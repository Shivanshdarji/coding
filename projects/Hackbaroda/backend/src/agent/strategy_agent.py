"""Synthesize all post analyses into a full content strategy report."""

import json
from datetime import datetime

from pydantic import BaseModel, Field

from src.agent.openai_client import call_structured
from src.models.content import ContentItem
from src.models.strategy import (
    ContentStrategyReport,
    DailyContentPlan,
    PostDeepAnalysis,
    PostingStrategy,
    WinningHook,
)

SYSTEM_PROMPT = """You are a senior, highly abstract Instagram growth strategist.
You receive scraped trending data and deep analyses of top-performing posts/reels.

Your job: produce a profoundly detailed, wide, and abstract 1-2 week content strategy.
You MUST write everything in a continuous, flowing passage format. DO NOT use bullet points, short lists, or rigid outlines. Write like a rich, atmospheric essay that a creator can absorb deeply.
Base every recommendation on patterns found in the scraped viral content, but elevate the language.
Prioritize reels when the data shows reels outperforming. Embed concrete examples seamlessly within the passages."""


class StrategyAIResponse(BaseModel):
    niche_detected: str
    executive_summary: str
    top_performing_formats: list[str]
    winning_hooks: list[WinningHook]
    viral_patterns: list[str]
    why_content_goes_viral: list[str]
    content_pillars: list[str]
    top_reels_breakdown: list[str]
    top_posts_breakdown: list[str]
    hashtag_strategy: list[str]
    posting_strategy: PostingStrategy
    content_dos: list[str]
    content_donts: list[str]
    weekly_plan: list[DailyContentPlan]
    detailed_recommendations: list[str]


def _summarize_scraped(items: list[ContentItem]) -> dict:
    reels = [i for i in items if i.is_video]
    posts = [i for i in items if not i.is_video]

    sections: dict[str, int] = {}
    for item in items:
        if item.section:
            sections[item.section] = sections.get(item.section, 0) + 1

    return {
        "total_scraped": len(items),
        "reels_count": len(reels),
        "posts_count": len(posts),
        "avg_likes": round(sum(i.likes for i in items) / len(items)) if items else 0,
        "avg_comments": round(sum(i.comments for i in items) / len(items)) if items else 0,
        "top_sections": sorted(sections.items(), key=lambda x: x[1], reverse=True)[:5],
        "top_creators": [f"@{i.username}" for i in sorted(items, key=lambda x: x.viral_score, reverse=True)[:5]],
    }


def _build_strategy_prompt(
    analyses: list[PostDeepAnalysis],
    all_items: list[ContentItem],
    weeks: int,
    niche: str | None,
) -> str:
    days = weeks * 7
    niche_hint = f"Target niche: {niche}" if niche else "Detect niche from scraped content"

    analyses_summary = []
    for a in analyses:
        analyses_summary.append({
            "rank": a.rank,
            "url": a.url,
            "username": a.username,
            "format": a.format_label,
            "how_it_was_made": a.how_it_was_made,
            "hook": a.hook_analysis,
            "why_viral": a.why_viral,
            "replication": a.replication_guide,
            "likes": a.scraped_data.likes,
            "comments": a.scraped_data.comments,
            "plays": a.scraped_data.plays,
        })

    return f"""Build a complete {weeks}-week ({days}-day) Instagram content strategy.

{niche_hint}

SCRAPED DATA SUMMARY:
{json.dumps(_summarize_scraped(all_items), indent=2)}

DEEP POST/REEL ANALYSES:
{json.dumps(analyses_summary, indent=2)}

Requirements for weekly_plan:
- Exactly {days} days (day_number 1 to {days})
- Each day needs: content_type, topic, hook, script_outline, caption_framework, hashtags, best_posting_time
- Reference inspiration_post_url from the analyses when relevant
- Mix reels and posts based on what performed best in the data
- Include specific hook scripts, not vague advice

Also provide:
- Top winning hook patterns with examples from the scraped content
- Why viral content is working right now in this niche
- Detailed posting strategy (frequency, best times, format mix)
- Content pillars to build around
- Do's and don'ts based on the data"""


def generate_strategy_report(
    analyses: list[PostDeepAnalysis],
    all_items: list[ContentItem],
    *,
    weeks: int = 2,
    niche: str | None = None,
) -> ContentStrategyReport:
    """Generate the final comprehensive content strategy."""
    response = call_structured(
        SYSTEM_PROMPT,
        _build_strategy_prompt(analyses, all_items, weeks, niche),
        StrategyAIResponse,
    )

    return ContentStrategyReport(
        generated_at=datetime.now(),
        niche_detected=response.niche_detected,
        executive_summary=response.executive_summary,
        top_performing_formats=response.top_performing_formats,
        winning_hooks=response.winning_hooks,
        viral_patterns=response.viral_patterns,
        why_content_goes_viral=response.why_content_goes_viral,
        content_pillars=response.content_pillars,
        top_reels_breakdown=response.top_reels_breakdown,
        top_posts_breakdown=response.top_posts_breakdown,
        hashtag_strategy=response.hashtag_strategy,
        posting_strategy=response.posting_strategy,
        content_dos=response.content_dos,
        content_donts=response.content_donts,
        weekly_plan=response.weekly_plan,
        detailed_recommendations=response.detailed_recommendations,
        per_post_analyses=analyses,
        scraped_summary=_summarize_scraped(all_items),
    )
