from pydantic import BaseModel, Field


class NormalizedService(BaseModel):
    service_id: str
    organization: str
    service_name: str
    category: str
    city: str
    address: str | None = None
    phone: str | None = None
    description: str | None = None
    source: str
    source_record_id: str
    keywords: list[str] = Field(default_factory=list)