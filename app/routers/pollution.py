from datetime import datetime
from typing import Dict, Union

from fastapi import APIRouter, Depends, Query, status, HTTPException

from app.db.repositories.city_repository import CityRepository
from app.db.repositories.pollution_repository import PollutionRepository
from app.dependencies import get_db, Session
from app.schemas.city import City as CitySchema
from app.schemas.pollution import (
    Pollution as PollutionSchema,
    PollutionItem,
    PollutionItemList,
)
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
    response_model=PollutionItemList,
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
) -> PollutionItemList:
    if end <= start:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="End time must be greater than start time",
        )
    city_repo = CityRepository(db)
    city = city_repo.get_city_by_lat_and_lon(lat, lon)
    if city:
        pollution_repo = PollutionRepository(db)
        pollution = pollution_repo.get_pollution(start, end, city.id)
        return PollutionItemList(
            data=[PollutionItem.from_orm(x) for x in pollution],
            city=CitySchema.from_orm(city),
        )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found")


@router.post(
    "/",
    operation_id="import_pollution_data_for_location",
    summary="Import pollution data",
)
async def import_historical_pollution_by_coords(
        pollution_params: PollutionSchema, db: Session = Depends(get_db)
) -> Dict[str, str]:
    city_repo = CityRepository(db)
    city = city_repo.search_city(
        pollution_params.name, pollution_params.lat, pollution_params.lon
    )
    if city is None:
        city_data = await get_cities(
            pollution_params.lat, pollution_params.lon, pollution_params.name
        )
        if city_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="City not found"
            )

        city = city_repo.create_city(city_data)

    if city:
        pollution_data = await fetch_pollution_by_coords(
            pollution_params.lat,
            pollution_params.lon,
            pollution_params.start,
            pollution_params.end,
            city.id,
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
) -> Dict[str, Union[bool, int]]:
    city_repo = CityRepository(db)
    city = city_repo.get_city_by_lat_and_lon(lat, lon)
    print(city)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    pollution_repo = PollutionRepository(db)
    result = pollution_repo.delete_pollution_range(start, end, city.id)
    return {"success": True, "deleted": result}
