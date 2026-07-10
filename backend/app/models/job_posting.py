from datetime import datetime

from pydantic import BaseModel, Field


class NormalizedJobPosting(BaseModel):
    posting_id: str
    source: str
    source_record_id: str

    title: str
    employer: str
    description: str
    location: str | None = None
    employment_type: str | None = None
    salary: str | None = None
    url: str | None = None
    posted_at: datetime | None = None

    skills: list[str] = Field(default_factory=list)
    organizations: list[str] = Field(default_factory=list)
    locations: list[str] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)