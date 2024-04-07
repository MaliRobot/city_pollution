from datetime import date, datetime
from typing import Any, Optional, List

from pydantic import BaseModel, Field, field_validator, ConfigDict
from pydantic_extra_types.coordinate import Longitude, Latitude

from app.schemas.city import City


class BasePollution(BaseModel):
    start: date = Field(..., description="Start time as date")
    end: date = Field(..., description="End time as date")

    @field_validator("start", "end")
    def validate_timestamp(cls, value: date) -> Any:
        unix_time_start = datetime.fromtimestamp(0).date()
        current_time = datetime.now().date()
        if value < unix_time_start or value > current_time:
            raise ValueError(
                "Timestamp must be within the valid range from the start of Unix time till now."
            )
        return value


class Pollution(BasePollution):
    lat: Latitude
    lon: Longitude
    name: str


class PollutionItem(BaseModel):
    id: int
    co: Optional[float]
    no: Optional[float]
    no2: Optional[float]
    o3: Optional[float]
    so2: Optional[float]
    pm2: Optional[float] = None
    pm10: Optional[float]
    nh3: Optional[float]
    date: Optional[date]
    city_id: int

    model_config = ConfigDict(from_attributes=True)


class PollutionItemList(BaseModel):
    data: List[PollutionItem]
    city: City
