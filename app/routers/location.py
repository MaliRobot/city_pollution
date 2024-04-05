from fastapi import APIRouter, Query

from app.services.location import get_location_by_name

router = APIRouter(
    prefix="/api/location",
    tags=["location"],
)


@router.get(
    "/name/",
    operation_id="get_location_by_name",
    summary="Get location data by location name",
)
async def get_location_coords_by_name(
        name: str = Query(..., description="Location name", min_length=1, max_length=255),
):
    return await get_location_by_name(name)
