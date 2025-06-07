from typing import Any
from abc import ABC, abstractmethod


class GeocoderServiceInterface(ABC):
    """Interface for geocoder service operations"""

    @abstractmethod
    async def get_reverse_geocode(self, lat: float, lon: float) -> Any:
        """Get reverse geocode data for coordinates"""
        pass

    @abstractmethod
    async def get_city_by_name(self, name: str) -> Any:
        """Get city data by name"""
        pass


class GeocoderService(GeocoderServiceInterface):
    """Service for geocoding operations"""

    def __init__(self, geocoder=None):
        self._geocoder = geocoder

    async def _get_geocoder(self):
        """Get geocoder instance, creating it if needed"""
        from city_pollution.dependencies import get_geocoder

        if self._geocoder is None:
            self._geocoder = await get_geocoder()
        return self._geocoder

    async def get_reverse_geocode(self, lat: float, lon: float) -> Any:
        """
        :param lat: Latitude
        :type: float
        :param lon: Longitude
        :type: float
        :return: list containing the dictionaries of all locations found under the lat/lon coordinates
        :rtype: Any
        """
        geocoder = await self._get_geocoder()
        locs_by_reverse = geocoder.reverse_geocode(lat, lon)
        return locs_by_reverse

    async def get_city_by_name(self, name: str) -> Any:
        """
        :param name: Name of the city
        :type: str
        :return: list containing the dictionaries of all locations found under the lat/lon coordinates
        :rtype: Any
        """
        geocoder = await self._get_geocoder()
        return geocoder.geocode(name)


# Legacy function wrappers for backward compatibility
async def get_reverse_geocode(lat: float, lon: float) -> Any:
    """Legacy function wrapper - deprecated, use GeocoderService instead"""
    service = GeocoderService()
    return await service.get_reverse_geocode(lat, lon)


async def get_city_by_name(name: str) -> Any:
    """Legacy function wrapper - deprecated, use GeocoderService instead"""
    service = GeocoderService()
    return await service.get_city_by_name(name)
