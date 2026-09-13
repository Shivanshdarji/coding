from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ContentItem(BaseModel):
    """Normalized Instagram content from any scraper source."""

    id: str
    url: str
    username: str
    caption: str = ""
    likes: int = 0
    comments: int = 0
    plays: int = 0
    is_video: bool = False
    content_type: str = "feed"  # clips, feed, carousel
    section: Optional[str] = None
    topic: Optional[str] = None
    hashtags: list[str] = Field(default_factory=list)
    image_url: Optional[str] = None
    video_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    duration: Optional[int] = None
    published_at: Optional[datetime] = None
    source: str = "unknown"  # trending, hashtag
    hashtag: Optional[str] = None
    is_verified: bool = False
    follower_count: Optional[int] = None
    audio_title: Optional[str] = None
    viral_score: float = 0.0
    engagement_rate: float = 0.0

    @property
    def total_engagement(self) -> int:
        return self.likes + self.comments + self.plays


class ContentSuggestion(BaseModel):
    """Ranked content suggestion with reasoning."""

    rank: int
    item: ContentItem
    why_trending: str
    content_ideas: list[str] = Field(default_factory=list)
