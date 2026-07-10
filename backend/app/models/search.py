from pydantic import BaseModel, Field


class InterpretedQuery(BaseModel):
    query: str
    categories: list[str] = Field(default_factory=list)
    locations: list[str] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)
    summary: str


class SearchResult(BaseModel):
    rank: int
    service_id: str
    service_name: str
    organization: str
    city: str
    category: str
    score: int
    match_reasons: list[str]


class SearchResponse(BaseModel):
    interpretation: InterpretedQuery
    results: list[SearchResult]
    answer: str
