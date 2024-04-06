from dataclasses import dataclass
from typing import List, Optional

from app.dependencies import Session
from app.entities.city import City


@dataclass
class CityRepository:
    db: Session

    def create_city(self, city: City) -> City | None:
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

    def update_city(self, city_id: int, city_data: dict) -> Optional[City]:
        city = self.db.query(City).filter(City.id == city_id).update(**city_data)
        self.db.flush()
        return city

    def delete_city(self, city_id: int) -> None:
        city = self.get_city_by_id(city_id)
        if city is not None:
            self.db.delete(city)
            self.db.commit()

    def get_cities(self, limit: int, offset: int) -> List:
        query = self.db.query(City)
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)
        return query.all()
