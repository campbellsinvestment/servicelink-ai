from pydantic import BaseModel


class AlbertaLocation(BaseModel):
    city: str
    province: str = "Alberta"
    province_code: str = "AB"
    country: str = "Canada"
    latitude: float | None = None
    longitude: float | None = None