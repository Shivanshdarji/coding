from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from src.models.content import ContentSuggestion
from src.models.strategy import ContentStrategyReport


class PipelineInput(BaseModel):
    """All inputs for the full scrape -> analyze -> strategy workflow."""

    niche: Optional[str] = Field(
        default=None,
        description="Creator niche e.g. fitness, music, travel",
    )
    country: str = Field(default="United States")
    hashtags: list[str] = Field(
        default_factory=list,
        description="Extra hashtags to scrape top posts from",
    )
    scrape_count: int = Field(
        default=50, ge=10, le=500,
        description="Number of trending Explore posts to scrape",
    )
    hashtag_scrape_count: int = Field(
        default=50, ge=24, le=200,
        description="Max posts per hashtag",
    )
    top_n: int = Field(
        default=5, ge=1, le=20,
        description="Top posts/reels to deep-analyze with OpenAI",
    )
    weeks: int = Field(default=2, ge=1, le=2)
    use_vision: bool = Field(
        default=True,
        description="Try thumbnail vision analysis (falls back to text if URLs expire)",
    )
    save_outputs: bool = Field(
        default=True,
        description="Save JSON files to output/ folder",
    )


class PipelineProgress(BaseModel):
    stage: str
    detail: str = ""
    timestamp: datetime = Field(default_factory=datetime.now)


class PipelineResult(BaseModel):
    """Complete output from the full pipeline."""

    status: str = "completed"
    input: PipelineInput
    progress_log: list[PipelineProgress] = Field(default_factory=list)
    scraped_count: int = 0
    suggestions: list[ContentSuggestion] = Field(default_factory=list)
    strategy_report: Optional[ContentStrategyReport] = None
    output_files: dict[str, str] = Field(default_factory=dict)
    elapsed_seconds: float = 0.0
