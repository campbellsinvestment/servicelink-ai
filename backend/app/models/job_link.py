from pydantic import BaseModel


class JobServiceLink(BaseModel):
    posting_id: str
    service_id: str
    score: int
    match_reasons: list[str]
