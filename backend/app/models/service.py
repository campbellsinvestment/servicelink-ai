from pydantic import BaseModel, Field
from backend.app.models.geography import AlbertaLocation

class NormalizedService(BaseModel):
    service_id: str
    organization: str
    service_name: str
    category: str
    city: str
    geography: AlbertaLocation | None = None
    address: str | None = None
    phone: str | None = None
    description: str | None = None
    source: str
    source_record_id: str
    keywords: list[str] = Field(default_factory=list)