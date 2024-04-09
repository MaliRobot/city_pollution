from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, Type

from city_pollution.entities.city import City


class ICityRepository(ABC):
    @abstractmethod
    def create_city(self, city: City) -> City:
        raise NotImplementedError

    @abstractmethod
    def search_city(self, city_name: str, lat: float, lon: float) -> City | None:
        raise NotImplementedError

    @abstractmethod
    def get_city_by_id(self, city_id: int) -> Optional[City]:
        raise NotImplementedError

    @abstractmethod
    def get_city_by_lat_and_lon(self, lat: float, lon: float) -> City | None:
        raise NotImplementedError

    @abstractmethod
    def update_city(self, city_id: int, city_data: Dict[Any, Any]) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete_city(self, city_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_cities(self, limit: int, offset: int) -> list[Type[City]]:
        raise NotImplementedError
