from typing import Iterator

from opencage.geocoder import OpenCageGeocode
from sqlalchemy.orm import Session

from city_pollution.config.settings import settings
from city_pollution.db.connection import session_maker
from city_pollution.services.geocoder_service import GeocoderService
from city_pollution.services.openweather_service import OpenWeatherService
from city_pollution.services.city import CityService
from city_pollution.services.pollution import PollutionService


def get_db() -> Iterator[Session]:
    _session_maker = session_maker()
    with _session_maker() as db:
        try:
            yield db
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()


async def get_geocoder() -> OpenCageGeocode:
    async with OpenCageGeocode(settings.opencage_key) as geocoder:
        return geocoder


# Service instances for dependency injection
_geocoder_service = None
_openweather_service = None
_city_service = None
_pollution_service = None


async def get_geocoder_service() -> GeocoderService:
    """Get or create GeocoderService instance"""
    global _geocoder_service
    if _geocoder_service is None:
        geocoder = await get_geocoder()
        _geocoder_service = GeocoderService(geocoder)
    return _geocoder_service


def get_openweather_service() -> OpenWeatherService:
    """Get or create OpenWeatherService instance"""
    global _openweather_service
    if _openweather_service is None:
        _openweather_service = OpenWeatherService()
    return _openweather_service


async def get_city_service() -> CityService:
    """Get or create CityService instance"""
    global _city_service
    if _city_service is None:
        geocoder_service = await get_geocoder_service()
        _city_service = CityService(geocoder_service)
    return _city_service


async def get_pollution_service() -> PollutionService:
    """Get or create PollutionService instance"""
    global _pollution_service
    if _pollution_service is None:
        openweather_service = get_openweather_service()
        city_service = await get_city_service()
        _pollution_service = PollutionService(openweather_service, city_service)
    return _pollution_service


__all__ = [
    "get_db",
    "get_geocoder",
    "get_geocoder_service",
    "get_openweather_service",
    "get_city_service",
    "get_pollution_service",
    "Session",
]
