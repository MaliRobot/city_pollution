from typing import Dict

from app.entities import City
from app.services.geocoder_service import get_reverse_geocode, get_city_by_name


def city_from_raw_data(raw_data: Dict) -> City | None:
    data = raw_data["components"]
    if data["_type"] == "city":
        city_name = data.get("city") or data.get("town")
        geometry = raw_data.get("geometry")
        if not city_name or not geometry:
            return None

        city = City(
            id=None,
            name=city_name,
            state=data.get("state"),
            country=data.get("country"),
            county=data.get("county"),
            lat=geometry.get("lat"),
            lon=geometry.get("lng"),
        )
        return city
    return None


async def get_city(lat: float, lon: float, city_name: str) -> City | None:
    city_by_geocode = await get_reverse_geocode(lat, lon)
    city_by_name = await get_city_by_name(city_name)
    all_cities = city_by_name + city_by_geocode
    if all_cities is not None:
        cities = [
            city_from_raw_data(loc)
            for loc in all_cities
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
