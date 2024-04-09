from dataclasses import dataclass
from typing import Optional, Dict, Any, List

from app.db.repositories.interfaces.city_repository import ICityRepository
from app.dependencies import Session
from app.entities.city import City


@dataclass
class CityRepository(ICityRepository):
    db: Session

    def create_city(self, city: City) -> City:
        db_city = self.search_city(city_name=city.name, lat=city.lat, lon=city.lon)
        if db_city:
            return city

        self.db.add(city)
        self.db.commit()
        self.db.refresh(city)
        return city

    def search_city(self, city_name: str, lat: float, lon: float) -> City | None:
        return (
            self.db.query(City)
            .filter_by(name=city_name, lat=lat, lon=lon)
            .one_or_none()
        )

    def get_city_by_id(self, city_id: int) -> Optional[City]:
        return self.db.query(City).get(city_id)

    def get_city_by_lat_and_lon(self, lat: float, lon: float) -> City | None:
        return self.db.query(City).filter_by(lat=lat, lon=lon).one_or_none()

    def update_city(self, city_id: int, city_data: Dict[Any, Any]) -> None:
        self.db.query(City).filter_by(id=city_id).update(**city_data)
        self.db.flush()

    def delete_city(self, city_id: int) -> bool:
        city = self.get_city_by_id(city_id)
        if city is not None:
            self.db.delete(city)
            self.db.commit()
            return True
        return False

    def get_cities(self, limit: int, offset: int) -> List[City]:
        query = self.db.query(City)
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)
        return query.all()
