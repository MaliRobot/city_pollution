from datetime import datetime
from typing import Dict, Union, Optional, List

from fastapi import APIRouter, Depends, Query, status, HTTPException

from city_pollution.db.repositories.city_repository import CityRepository
from city_pollution.db.repositories.pollution_repository import PollutionRepository
from city_pollution.dependencies import get_db, Session
from city_pollution.entities import Pollution, City
from city_pollution.schemas.city import City as CitySchema
from city_pollution.schemas.pollution import (
    Pollution as PollutionSchema,
    PollutionItem,
    PollutionItemList,
    Dates,
    Aggregate,
)
from city_pollution.services.city import get_city
from city_pollution.services.pollution import (
    fetch_pollution_by_coords,
    aggregated_pollutions,
    generate_pollution_plot,
)

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
    "Has limit and offset parameters for possibility of pagination for front end",
)
async def get_pollution_data(
    aggregate: Aggregate = Aggregate.DAILY,
    city_id: int = Query(..., description="Id of city to get pollution data for"),
    dates: Dates = Depends(),
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    db: Session = Depends(get_db),
) -> PollutionItemList:
    city_repo = CityRepository(db)
    city = city_repo.get_city_by_id(city_id)

    if city and city.id:
        pollution_repo = PollutionRepository(db)
        if aggregate != Aggregate.DAILY:
            pollutions = pollution_repo.get_pollution(dates.start, dates.end, city.id)
            agg_pollution, gaps = aggregated_pollutions(
                pollutions, city.id, aggregate.value
            )
            result = await pollution_response_handler(agg_pollution, city, gaps)
            return result

        pollution = pollution_repo.get_pollution(
            dates.start, dates.end, city.id, limit, offset
        )
        result = await pollution_response_handler(pollution, city)
        return result
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found")


async def pollution_response_handler(
    pollution: List[Pollution], city: City, gaps: bool = False
) -> PollutionItemList:
    """
    Prepare response for pollution data request
    :param pollution: List of Pollution instances
    :type pollution: List[Pollution]
    :param city: City instance
    :type city: City
    :param gaps: True if there is gap between the dates in the data, otherwise False or None
    :type gaps: bool
    :return: Returns PollutionItemList containing pollution data, date range for data and gaps flag
    :rtype: List[PollutionItemList]
    """
    start_dt = end_dt = None
    plot_url = None

    if len(pollution) > 0:
        start_dt = pollution[0].date
        end_dt = pollution[-1].date
        plot_url = generate_pollution_plot(pollution, city)

    return PollutionItemList(
        data=[PollutionItem.model_validate(x) for x in pollution],
        city=CitySchema.model_validate(city),
        start=start_dt,
        end=end_dt,
        gaps=gaps,
        plot_url=plot_url,
    )


@router.post(
    "/",
    operation_id="import_pollution_data_for_location",
    summary="Import pollution data",
    description="Import pollution for given location. Location must match city or town"
    "that is fetched from external service if it's not already in database"
    "Then pollution data is fetched from external service. Old pollution data is deleted if"
    "exists for a given city/town.",
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

    if city and city.id:
        start_ts = int(
            datetime.combine(
                pollution_params.dates.start, datetime.min.time()
            ).timestamp()
        )
        end_ts = int(
            datetime.combine(
                pollution_params.dates.end, datetime.min.time()
            ).timestamp()
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
    description="Delete pollution data for given city.",
)
async def delete_pollution_data(
    city_id: int,
    dates: Dates = Depends(),
    db: Session = Depends(get_db),
) -> Dict[str, Union[bool, int]]:
    city_repo = CityRepository(db)
    city = city_repo.get_city_by_id(city_id)
    if city and city.id:
        pollution_repo = PollutionRepository(db)
        result = pollution_repo.delete_pollution_range(dates.start, dates.end, city.id)
        return {"success": True, "deleted": result}
    raise HTTPException(status_code=404, detail="City not found")
