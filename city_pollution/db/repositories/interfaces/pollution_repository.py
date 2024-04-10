from abc import ABC, abstractmethod
from datetime import date
from typing import List, Optional, Any, Dict

from city_pollution.entities.pollution import Pollution


class IPollutionRepository(ABC):
    @abstractmethod
    def create_pollution(self, pollution_data: List[Pollution]) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_pollution_by_id(self, pollution_id: int) -> Any:
        raise NotImplementedError

    @abstractmethod
    def get_pollution(
        self,
        start: date,
        end: date,
        city_id: int,
        limit: Optional[int],
        offset: Optional[int],
    ) -> List[Pollution]:
        raise NotImplementedError

    @abstractmethod
    def update_pollution(
        self, pollution_id: int, pollution_data: Dict[str, Any]
    ) -> Optional[Pollution]:
        raise NotImplementedError

    @abstractmethod
    def delete_pollution_range(self, start: date, end: date, city_id: int) -> int:
        raise NotImplementedError
