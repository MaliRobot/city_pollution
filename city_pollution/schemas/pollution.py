from datetime import date, datetime
from enum import Enum
from typing import Optional, List

from fastapi import HTTPException, status
from pydantic import BaseModel, Field, ConfigDict, model_validator
from pydantic_extra_types.coordinate import Longitude, Latitude

from city_pollution.schemas.city import City


class Dates(BaseModel):
    start: date = Field(..., description="Start time as date")
    end: date = Field(..., description="End time as date")

    @model_validator(mode="before")
    def validate_dates(cls, values: dict[str, date]) -> dict[str, date]:
        """
        Validate dates
        :param values:
        :return:
        """
        start_date = values.get("start")
        end_date = values.get("end")
        if start_date is None or end_date is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Start and end dates are both required.",
            )
        current_date = datetime.now().date()

        try:
            if isinstance(start_date, str):
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()

            if isinstance(end_date, str):
                end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid date format",
            )

        if end_date > current_date:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="End date cannot be in the future",
            )
        if start_date > end_date:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="End date must be greater than or equal to start date",
            )

        return values


class Pollution(BaseModel):
    lat: Latitude
    lon: Longitude
    dates: Dates
    name: str


class PollutionItem(BaseModel):
    id: Optional[int] = None
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
    start: Optional[date]
    end: Optional[date]
    gaps: Optional[bool] = None


class Aggregate(Enum):
    DAILY = "daily"
    MONTHLY = "monthly"
    YEARLY = "yearly"
