from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod

from city_pollution.entities import City
from city_pollution.services.geocoder_service import GeocoderService

TOLERANCE = 0.5  # degrees


class CityServiceInterface(ABC):
    """Interface for city service operations"""

    @abstractmethod
    async def get_city(
        self, lat: float, lon: float, city_name: Optional[str] = None
    ) -> City | None:
        """Get city by coordinates and optional name"""
        pass

    @abstractmethod
    def city_from_raw_data(self, raw_data: Dict[Any, Any]) -> City | None:
        """Convert raw geocoder data to City entity"""
        pass

    @abstractmethod
    async def extract_cities_from_raw_data(
        self, cities_raw_data: Dict[Any, Any]
    ) -> List[City | None]:
        """Extract cities from raw geocoder response"""
        pass


class CityService(CityServiceInterface):
    """Service for city-related operations"""

    def __init__(self, geocoder_service: GeocoderService):
        self.geocoder_service = geocoder_service

    def city_from_raw_data(self, raw_data: Dict[Any, Any]) -> City | None:
        """
        Instantiate City object from raw_data dictionary
        :param raw_data: Dictionary containing raw city data
        :return: City object
        :rtype: City | None
        """
        data = raw_data["components"]
        if data["_type"] == "city" or data.get("city"):
            city_name = data.get("city") or data.get("town")
            geometry = raw_data.get("geometry")
            if not city_name or not geometry:
                return None

            city = City(
                id=None,
                name=city_name,
                state=data.get("state"),  # Now optional
                country=data.get("country"),
                county=data.get("county"),
                lat=geometry.get("lat"),
                lon=geometry.get("lng"),
            )
            return city
        return None

    async def extract_cities_from_raw_data(
        self, cities_raw_data: Dict[Any, Any]
    ) -> List[City | None]:
        print(cities_raw_data)
        return [
            self.city_from_raw_data(loc)
            for loc in cities_raw_data
            if "city" in loc["components"]
            or loc["components"]["_type"] in ["city", "town"]
        ]

    async def get_city(
        self, lat: float, lon: float, city_name: Optional[str] = None
    ) -> City | None:
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
        city_by_geocode = await self.geocoder_service.get_reverse_geocode(lat, lon)
        city_by_name = []
        if city_name:
            city_by_name = await self.geocoder_service.get_city_by_name(city_name)
        all_cities = city_by_name + city_by_geocode
        if all_cities is not None:
            cities = await self.extract_cities_from_raw_data(all_cities)

            for city in cities:
                if (
                    city is not None
                    and abs(city.lat - lat) < TOLERANCE
                    and abs(city.lon - lon) < TOLERANCE
                ):
                    return city
        return None


# Legacy function wrappers for backward compatibility
def city_from_raw_data(raw_data: Dict[Any, Any]) -> City | None:
    """Legacy function wrapper - deprecated, use CityService instead"""
    from city_pollution.services.geocoder_service import get_geocoder
    import asyncio

    async def _get_service():
        geocoder = await get_geocoder()
        geocoder_service = GeocoderService(geocoder)
        return CityService(geocoder_service)

    service = asyncio.run(_get_service())
    return service.city_from_raw_data(raw_data)


async def extract_cities_from_raw_data(
    cities_raw_data: Dict[Any, Any]
) -> List[City | None]:
    """Legacy function wrapper - deprecated, use CityService instead"""
    from city_pollution.services.geocoder_service import get_geocoder

    geocoder = await get_geocoder()
    geocoder_service = GeocoderService(geocoder)
    service = CityService(geocoder_service)
    return await service.extract_cities_from_raw_data(cities_raw_data)


async def get_city(
    lat: float, lon: float, city_name: Optional[str] = None
) -> City | None:
    """Legacy function wrapper - deprecated, use CityService instead"""
    from city_pollution.services.geocoder_service import get_geocoder

    geocoder = await get_geocoder()
    geocoder_service = GeocoderService(geocoder)
    service = CityService(geocoder_service)
    return await service.get_city(lat, lon, city_name)
