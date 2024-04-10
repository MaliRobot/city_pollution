from typing import Dict, Any

from city_pollution.entities import City
from city_pollution.services.geocoder_service import (
    get_reverse_geocode,
    get_city_by_name,
)

TOLERANCE = 0.5


def city_from_raw_data(raw_data: Dict[Any, Any]) -> City | None:
    """
    Instantiate City object from raw_data dictionary
    :param raw_data: Dictionary containing raw city data
    :return: City object
    :rtype: City | None
    """
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
    """
    Search for the city using the geocoder with given city name,
    latitude and longitude. Preprocess data using other functions
    and filter the results looking for the match against the
    city name and coordinates. We use certain tolerance when
    matching coordinates, because they rarely perfectly match.
    :param lat: Latitude of the city
    :param lon: Longitude of the city
    :param city_name: City name
    :return:
    """
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
                and abs(city.lat - lat) < TOLERANCE
                and abs(city.lon - lon) < TOLERANCE
            ):
                return city
    return None
