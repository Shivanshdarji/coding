from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from src.models.content import ContentItem


class PostDeepAnalysis(BaseModel):
    """AI-generated deep breakdown of a single post or reel."""

    rank: int
    url: str
    username: str
    content_type: str
    format_label: str = Field(description="e.g. Reel, Carousel, Single Image Post")
    how_it_was_made: str = Field(description="Step-by-step production breakdown")
    hook_analysis: str = Field(description="Opening hook and why it stops the scroll")
    caption_breakdown: str = Field(description="Caption structure, tone, and CTA analysis")
    visual_style: str = Field(description="Visual aesthetic, editing, pacing, layout")
    audio_strategy: Optional[str] = Field(default=None, description="Music/sound/voiceover strategy")
    why_viral: list[str] = Field(default_factory=list)
    engagement_insights: str = Field(description="What the metrics reveal about audience response")
    replication_guide: list[str] = Field(default_factory=list)
    key_takeaways: list[str] = Field(default_factory=list)
    scraped_data: ContentItem


class PostingStrategy(BaseModel):
    frequency: str = Field(description="How often to post per week")
    best_times: list[str] = Field(description="Best posting times")
    format_mix: str = Field(description="Ratio of reels vs posts vs carousels")
    engagement_tactics: list[str] = Field(default_factory=list)


class WinningHook(BaseModel):
    pattern: str
    example_from_scrape: str
    why_it_works: str
    how_to_use: str


class DailyContentPlan(BaseModel):
    day: str
    day_number: int
    content_type: str
    topic: str
    hook: str
    script_outline: str
    caption_framework: str
    hashtags: list[str] = Field(default_factory=list)
    best_posting_time: str
    inspiration_post_url: Optional[str] = None


class ContentStrategyReport(BaseModel):
    """Full content strategy output from the agent."""

    generated_at: datetime = Field(default_factory=datetime.now)
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
    per_post_analyses: list[PostDeepAnalysis]
    scraped_summary: dict


class MockAdvertisement(BaseModel):
    title: str
    description: str
    image_base64: str
    suggested_caption: str
    ad_type: str  # "story_post", "product_highlight", "reel_thumbnail"
    hashtags: list[str] = []
    prompt_used: str = ""
