from typing import Any, Optional, List

from fastapi import APIRouter, Query, Depends, HTTPException

from app.db.repositories.city_repository import CityRepository
from app.dependencies import Session, get_db
from app.schemas.city import City
from app.services.city import get_city_by_name

router = APIRouter(
    prefix="/api/city",
    tags=["city"],
)


@router.get(
    "/",
    operation_id="get_all_cities_from_database",
    summary="Get all cities from the database",
    description="Gets all cities currently stored in the database. Provides limit and offset parameters for pagination.",
)
def get_cities_list(
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    db: Session = Depends(get_db),
) -> List[City]:
    city_repo = CityRepository(db)
    return city_repo.get_cities(limit=limit, offset=offset)


@router.get(
    "/name/",
    operation_id="get_city_by_name",
    summary="Get city data by name",
    description="Get city data by name",
)
async def get_city_coords_by_name(
    name: str = Query(..., description="City name", min_length=1, max_length=255),
) -> Any:
    return await get_city_by_name(name)


@router.delete(
    "/{city_id}/",
    operation_id="delete_city_by_id",
    summary="Delete city by id and its data",
    description="Deletes a city by id and all its pollution data",
)
async def delete_city(city_id: int, db: Session = Depends(get_db)) -> Any:
    city_repo = CityRepository(db)
    result = city_repo.delete_city(city_id)
    if result:
        return {"message": "City deleted successfully"}
    raise HTTPException(status_code=404, detail="Delete failed, city not found")
