from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator
from pydantic_extra_types.coordinate import Longitude, Latitude


class BasePollution(BaseModel):
    start: int = Field(..., description="Start time as timestamp")
    end: int = Field(..., description="End time as timestamp")

    @field_validator("start", "end")
    def validate_timestamp(cls, value: int) -> Any:
        unix_time_start = 0
        current_time = datetime.now().timestamp()
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
    co: float
    no: float
    no2: float
    o3: float
    so2: float
    pm2: float
    pm10: float
    nh3: float
    timestamp: int
    site_id: int
