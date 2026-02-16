"""Data models for LinkedIn posts and media."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class Media:
    """Represents a media attachment (image, video, or document)."""

    type: str  # 'image', 'video', 'document'
    url: str
    local_path: Optional[str] = None
    filename: Optional[str] = None

    def __post_init__(self):
        """Validate media type."""
        valid_types = ['image', 'video', 'document']
        if self.type not in valid_types:
            raise ValueError(f"Media type must be one of {valid_types}, got: {self.type}")


@dataclass
class LinkedInPost:
    """Represents a LinkedIn post with all its metadata."""

    id: str
    post_url: str
    content: str
    created_at: datetime
    post_type: str  # 'original', 'repost', 'article', 'poll'
    media: List[Media] = field(default_factory=list)
    hashtags: List[str] = field(default_factory=list)
    original_post_url: Optional[str] = None  # For reposts
    repost_commentary: Optional[str] = None  # Your addition to a repost
    slug: Optional[str] = None
    author_name: Optional[str] = None
    author_headline: Optional[str] = None

    def __post_init__(self):
        """Validate post type."""
        valid_types = ['original', 'repost', 'article', 'poll']
        if self.post_type not in valid_types:
            raise ValueError(f"Post type must be one of {valid_types}, got: {self.post_type}")

    def is_repost(self) -> bool:
        """Check if this is a repost."""
        return self.post_type == 'repost'

    def has_media(self) -> bool:
        """Check if post has any media attachments."""
        return len(self.media) > 0
