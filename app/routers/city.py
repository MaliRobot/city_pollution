from fastapi import APIRouter, Query

from app.services.city import get_city_by_name

router = APIRouter(
    prefix="/api/city",
    tags=["city"],
)


@router.get(
    "/name/",
    operation_id="get_city_by_name",
    summary="Get city data by name",
)
async def get_city_coords_by_name(
    name: str = Query(..., description="City name", min_length=1, max_length=255),
):
    return await get_city_by_name(name)
