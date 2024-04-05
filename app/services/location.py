from typing import List

from app.dependencies import get_geocoder
from app.entities.city import City


async def get_locations(lat: float, lon: float, name: str) -> City | None:
    geocoder = await get_geocoder()
    locs_by_reverse = geocoder.reverse_geocode(lat, lon)
    all_locations = [City.from_raw_data(loc) for loc in locs_by_reverse if
                     loc["components"]["_type"] in ["city", "town"]]
    if not all_locations:
        locations_by_name = await get_location_by_name(name)
        cities = [City.from_raw_data(loc) for loc in locations_by_name if
                  loc["components"]["_type"] in ["city", "town"]]
        for city in cities:
            if city != None and abs(city.lat - lat) < 0.5 and abs(city.lon - lon) < 0.5:
                return city
    return None


async def get_location_by_name(name: str) -> List[City]:
    geocoder = await get_geocoder()
    return geocoder.geocode(name)
