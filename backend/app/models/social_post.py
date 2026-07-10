from datetime import datetime

from pydantic import BaseModel, Field


class NormalizedSocialPost(BaseModel):
    post_id: str
    source: str
    source_record_id: str

    title: str | None = None
    body: str
    author: str | None = None
    community: str | None = None
    url: str | None = None

    created_at: datetime | None = None

    organizations: list[str] = Field(default_factory=list)
    locations: list[str] = Field(default_factory=list)
    service_categories: list[str] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)