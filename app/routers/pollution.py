from datetime import datetime

from fastapi import APIRouter, Depends, Query, status, HTTPException

from app.db.repositories.city_repository import CityRepository
from app.db.repositories.pollution_repository import PollutionRepository
from app.dependencies import get_db, Session
from app.schemas.pollution import Pollution
from app.services.city import get_cities
from app.services.pollution import fetch_pollution_by_coords

router = APIRouter(
    prefix="/api/pollution",
    tags=["pollution"],
)


@router.get(
    "/",
    operation_id="get_pollution_by_coordinates",
    summary="Get pollution data by coordinates",
)
async def get_pollution_data(
    lat: float = Query(..., description="Latitude", ge=-90, le=90),
    lon: float = Query(..., description="Longitude", ge=-180, le=180),
    start: int = Query(
        ...,
        description="Start time as timestamp",
        ge=0,
        lt=int(datetime.now().timestamp()),
    ),
    end: int = Query(
        ..., description="End time as timestamp", le=int(datetime.now().timestamp())
    ),
    db: Session = Depends(get_db),
):
    if end <= start:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="End time must be greater than start time",
        )
    return {}


@router.post(
    "/",
    operation_id="import_pollution_data_for_location",
    summary="Import pollution data",
)
async def import_historical_pollution_by_coords(
    pollution_params: Pollution, db: Session = Depends(get_db)
):
    city_data = await get_cities(
        pollution_params.lat, pollution_params.lon, pollution_params.name
    )
    if city_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="City not found"
        )
    city_repo = CityRepository(db)
    city = city_repo.create_city(city_data)

    if city:
        pollution_data = await fetch_pollution_by_coords(
            pollution_params.lat,
            pollution_params.lon,
            pollution_params.start,
            pollution_params.end,
        )

        if pollution_data:
            pollution_repo = PollutionRepository(db)
            pollution_repo.create_pollution(pollution_data)
            return {
                "success": f"pollution data imported for city {city.name} at coords {city.lat} {city.lon}"
            }
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Pollution data not found"
        )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found")


@router.delete(
    "/",
    operation_id="delete_pollution_data",
    summary="Delete pollution data",
)
async def delete_pollution_data(
    lat: float = Query(..., description="Latitude", ge=-90, le=90),
    lon: float = Query(..., description="Longitude", ge=-180, le=180),
    start: int = Query(
        ...,
        description="Start time as timestamp",
        ge=0,
        lt=int(datetime.now().timestamp()),
    ),
    end: int = Query(
        ..., description="End time as timestamp", le=int(datetime.now().timestamp())
    ),
    db: Session = Depends(get_db),
):
    return {}
