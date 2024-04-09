from datetime import datetime
from typing import Dict, Union, Optional

from fastapi import APIRouter, Depends, Query, status, HTTPException

from app.db.repositories.city_repository import CityRepository
from app.db.repositories.pollution_repository import PollutionRepository
from app.dependencies import get_db, Session
from app.schemas.city import City as CitySchema
from app.schemas.pollution import (
    Pollution as PollutionSchema,
    PollutionItem,
    PollutionItemList, Dates,
    Aggregate
)
from app.services.city import get_city
from app.services.pollution import fetch_pollution_by_coords, aggregated_pollutions

router = APIRouter(
    prefix="/api/pollution",
    tags=["pollution"],
)


@router.get(
    "/",
    operation_id="get_pollution_by_coordinates",
    summary="Get pollution data by coordinates",
    response_model=PollutionItemList,
    description="Get pollution data by coordinates provided that coordinates match any city or town."
                "Loads only data from the database, ie, what is imported so far from external services."
                "Has limit and offset parameters for possibility of pagination for front end"
)
async def get_pollution_data(
        aggregate: Aggregate = None,
        city_id: int = Query(..., description="Id of city to get pollution data for"),
        dates: Dates = Depends(),
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        db: Session = Depends(get_db),
) -> PollutionItemList:
    city_repo = CityRepository(db)
    city = city_repo.get_city_by_id(city_id)

    if city is not None:
        pollution_repo = PollutionRepository(db)
        if aggregate:
            pollutions = pollution_repo.get_pollution(dates.start, dates.end, city.id)
            agg_pollution = aggregated_pollutions(pollutions, city.id, aggregate)
            return PollutionItemList(
                data=[PollutionItem.model_validate(x) for x in agg_pollution],
                city=CitySchema.model_validate(city),
            )

        pollution = pollution_repo.get_pollution(dates.start, dates.end, city.id, limit, offset)
        return PollutionItemList(
            data=[PollutionItem.model_validate(x) for x in pollution],
            city=CitySchema.model_validate(city),
        )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found")


@router.post(
    "/",
    operation_id="import_pollution_data_for_location",
    summary="Import pollution data",
    description="Import pollution for given location. Location must match city or town"
                "that is fetched from external service if it's not already in database"
                "Then pollution data is fetched from external service. Old pollution data is deleted if"
                "exists for a given city/town."
)
async def import_historical_pollution_by_coords(
        pollution_params: PollutionSchema, db: Session = Depends(get_db)
) -> Dict[str, str]:
    city_repo = CityRepository(db)
    city = city_repo.search_city(
        pollution_params.name, pollution_params.lat, pollution_params.lon
    )

    if city is None:
        city_data = await get_city(
            pollution_params.lat, pollution_params.lon, pollution_params.name
        )
        if city_data:
            city = city_repo.create_city(city_data)

    if city:
        start_ts = int(
            datetime.combine(pollution_params.dates.start, datetime.min.time()).timestamp()
        )
        end_ts = int(
            datetime.combine(pollution_params.dates.end, datetime.min.time()).timestamp()
        )
        pollution_repo = PollutionRepository(db)
        pollution_repo.delete_pollution_range(
            pollution_params.dates.start, pollution_params.dates.end, city.id
        )
        pollution_data = await fetch_pollution_by_coords(
            pollution_params.lat,
            pollution_params.lon,
            start_ts,
            end_ts,
            city.id,
        )

        if pollution_data:
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
    description="Delete pollution data for given city and coordinates."
)
async def delete_pollution_data(
        lat: float = Query(..., description="Latitude", ge=-90, le=90),
        lon: float = Query(..., description="Longitude", ge=-180, le=180),
        dates: Dates = Depends(),
        db: Session = Depends(get_db),
) -> Dict[str, Union[bool, int | None]]:
    city_repo = CityRepository(db)
    city = city_repo.get_city_by_lat_and_lon(lat, lon)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    pollution_repo = PollutionRepository(db)
    result = pollution_repo.delete_pollution_range(dates.start, dates.end, city.id)
    return {"success": True, "deleted": result}
