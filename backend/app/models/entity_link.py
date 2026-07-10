from pydantic import BaseModel


class ServiceLink(BaseModel):
    post_id: str
    service_id: str
    score: int
    match_reasons: list[str]
