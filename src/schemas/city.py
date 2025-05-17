from typing import Optional

from pydantic import BaseModel, ConfigDict


class City(BaseModel):
    name: str
    state: str
    country: str
    lon: float
    lat: float
    time_created: int
    time_updated: Optional[int] = None
    county: Optional[str] = None
    id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
