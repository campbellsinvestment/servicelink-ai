from pydantic import BaseModel


class ServiceRecommendation(BaseModel):
    rank: int
    post_id: str
    post_title: str | None
    service_id: str
    service_name: str
    organization: str
    city: str
    category: str
    score: int
    match_reasons: list[str]
