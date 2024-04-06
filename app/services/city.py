from typing import Optional, Any

from app.dependencies import get_geocoder
from app.entities.city import City, city_factory


async def get_cities(lat: float, lon: float, name: str) -> Optional[City]:
    geocoder = await get_geocoder()
    locs_by_reverse = geocoder.reverse_geocode(lat, lon)
    all_locations = [
        city_factory(loc)
        for loc in locs_by_reverse
        if loc["components"]["_type"] in ["city", "town"]
    ]
    if not all_locations:
        locations_by_name = await get_city_by_name(name)
        cities = [
            city_factory(loc)
            for loc in locations_by_name
            if loc["components"]["_type"] in ["city", "town"]
        ]
        for city in cities:
            if (
                city is not None
                and abs(city.lat - lat) < 0.5
                and abs(city.lon - lon) < 0.5
            ):
                return city
    return None


async def get_city_by_name(name: str) -> Any:
    geocoder = await get_geocoder()
    return geocoder.geocode(name)
