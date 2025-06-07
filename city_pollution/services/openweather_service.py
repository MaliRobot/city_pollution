from typing import List, Dict, Any
from abc import ABC, abstractmethod

from fastapi import HTTPException
from httpx import AsyncClient

from city_pollution.config.settings import settings


class OpenWeatherServiceInterface(ABC):
    """Interface for OpenWeather service operations"""

    @abstractmethod
    async def get_pollution_data(
        self, lat: float, lon: float, start: int, end: int
    ) -> List[Dict[str, Any]]:
        """Get pollution data from OpenWeather API"""
        pass


class OpenWeatherService(OpenWeatherServiceInterface):
    """Service for OpenWeather API operations"""

    def __init__(self, api_key: str = None, base_url: str = None):
        self.api_key = api_key or settings.openweather_key
        self.base_url = base_url or settings.openweather_url

    async def get_pollution_data(
        self, lat: float, lon: float, start: int, end: int
    ) -> List[Dict[str, Any]]:
        """
        Retrieve data from OpenWeatherMap and process it to get pollution data
        :param lat: Latitude
        :type: float
        :param lon: Longitude
        :type: float
        :param start: starting point for pollution data
        :type: int
        :param end: ending point for pollution data
        :type: int
        :return: list of pollution data in dictionary format
        :rtype: List[Dict[str, Any]]
        """
        async with AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}?lat={lat}&lon={lon}&start={start}&end={end}&appid={self.api_key}"
            )

        if response.status_code == 200:
            pollutions_list = []
            if len(response.json()["list"]) > 0:
                pollutions = response.json()["list"]
                for pollution in pollutions:
                    d = pollution["components"]
                    d["timestamp"] = pollution["dt"]
                    pollutions_list.append(d)
                return pollutions_list
        raise HTTPException(
            status_code=response.status_code, detail="Couldn't retrieve pollution data"
        )


# Legacy function wrapper for backward compatibility
async def get_pollution_data(
    lat: float, lon: float, start: int, end: int
) -> List[Dict[str, Any]]:
    """Legacy function wrapper - deprecated, use OpenWeatherService instead"""
    service = OpenWeatherService()
    return await service.get_pollution_data(lat, lon, start, end)
