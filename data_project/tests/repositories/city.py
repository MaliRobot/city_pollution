import random
from datetime import datetime
from typing import ClassVar, Dict, Any, List

from data_project.db.repositories.interfaces.city_repository import ICityRepository
from data_project.entities import City


class CityFactory:
    _id: ClassVar[int] = 0

    @classmethod
    def create(cls, lat: float = None, lon: float = None) -> City:
        cls._id += 1
        city = f"name {random.randint(1, 100000)}"
        state = f"state {random.randint(1, 100000)}"
        country = f"country {random.randint(1, 100000)}"
        county = f"county {random.randint(1, 100000)}"
        if lat is None:
            lat = random.uniform(-90.0, 90.0)
        if lon is None:
            lon = random.uniform(-180.0, 180.0)

        return City(
            id=cls._id,
            name=city,
            state=state,
            country=country,
            county=county,
            lat=lat,
            lon=lon,
            time_created=random.randint(1, 100000),
        )


class CityRepositoryPrepopulated(ICityRepository):
    def __init__(self, _=None):
        self.cities = [
            City(
                id=1,
                name="San Francisco",
                state="California",
                country="United States",
                county=None,
                lat=40.53,
                lon=-74.56,
                time_created=176383940,
            ),
            City(
                id=2,
                name="Hanoi",
                state="Vietnam",
                country="Vietnam",
                county=None,
                lat=21.02,
                lon=-105.80,
                time_created=176383940,
            ),
        ]

    def create_city(self, city: City) -> City:
        db_city = self.search_city(city_name=city.name, lat=city.lat, lon=city.lon)
        if db_city:
            return city

        city.id = len(self.cities) + 1
        self.cities.append(city)
        return city

    def get_city_by_lat_and_lon(self, lat, lon) -> City | None:
        for city in self.cities:
            if city.lat == lat and city.lon == lon:
                return city
        return None

    def search_city(self, city_name: str, lat: float, lon: float) -> City | None:
        for city in self.cities:
            if city.lat == lat and city.lon == lon and city.name == city_name:
                return city
        return None

    def get_city_by_id(self, city_id: int) -> City | None:
        for city in self.cities:
            if city.id == city_id:
                return city
        return None

    def update_city(self, city_id: int, city_data: Dict[Any, Any]) -> None:
        for city in self.cities:
            if city.id == city_id:
                city.name = city_data["name"]
                city.lat = city_data["lat"]
                city.lon = city_data["lon"]
                city.state = city_data["state"]
                city.country = city_data["country"]
                city.county_code = city_data["county"]
                city.time_updated = datetime.now().date()
                break

    def delete_city(self, city_id: int) -> bool:
        for city in self.cities:
            if city.id == city_id:
                self.cities.remove(city)
                return True
        return False

    def get_cities(self, limit: int, offset: int) -> List[City]:
        if offset:
            cities = self.cities[offset:]
        else:
            cities = self.cities

        if limit is not None:
            cities = cities[:limit]

        return cities
