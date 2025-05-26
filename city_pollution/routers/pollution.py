from typing import Dict, Union, Optional

from fastapi import APIRouter, Depends, Query, status, HTTPException

from city_pollution.dependencies import get_db, Session

from city_pollution.schemas.pollution import (
    PollutionSchema,
    PollutionItemList,
    Dates,
    Aggregate,
)

from city_pollution.services.pollution import (
    get_pollution_data_service,
    import_historical_pollution,
    delete_pollution_data_service,
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
    try:
        return await get_pollution_data_service(
            aggregate, city_id, dates, db, limit, offset
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


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
    try:
        return await import_historical_pollution(pollution_params, db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


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
    try:
        return await delete_pollution_data_service(city_id, dates, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
