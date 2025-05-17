import random
from datetime import date
from typing import ClassVar, List, Optional, Dict, Any

from src.db.repositories.interfaces.pollution_repository import IPollutionRepository
from entities import Pollution


class PollutionFactory:
    _id: ClassVar[int] = 0

    @classmethod
    def create(cls, p_date: date, city_id: int) -> Pollution:
        cls._id += 1

        return Pollution(
            id=cls._id,
            co=random.uniform(0, 30),
            no=random.uniform(0, 100),
            no2=random.uniform(0, 100),
            o3=random.uniform(0, 100),
            so2=random.uniform(0, 100),
            pm2_5=random.uniform(0, 100),
            pm10=random.uniform(0, 100),
            nh3=random.uniform(0, 100),
            date=p_date,
            city_id=city_id,
        )


class PollutionRepositoryPrepopulated((IPollutionRepository)):
    def __init__(self, _=None) -> None:
        self.pollutions = [
            Pollution(
                id=1,
                co=100,
                no=0.0,
                no2=11.0,
                o3=25.0,
                so2=7.5,
                pm2_5=33.0,
                pm10=1.0,
                nh3=0.5,
                date=date(2024, 1, 1),
                city_id=1,
            ),
            Pollution(
                id=2,
                co=100,
                no=0.0,
                no2=12.0,
                o3=23.0,
                so2=6.5,
                pm2_5=53.0,
                pm10=1.0,
                nh3=0.5,
                date=date(2024, 1, 2),
                city_id=1,
            ),
            Pollution(
                id=3,
                co=34,
                no=10.0,
                no2=45.0,
                o3=23.0,
                so2=6.5,
                pm2_5=53.0,
                pm10=1.0,
                nh3=0.5,
                date=date(2024, 1, 2),
                city_id=2,
            ),
        ]

    def get_pollution(
        self,
        start: date,
        end: date,
        city_id: int,
        limit: int = None,
        offset: int = None,
    ) -> List[Pollution]:
        result = [
            x
            for x in self.pollutions
            if x.city_id == city_id and (start <= x.date <= end)
        ]

        if offset:
            result = result[offset:]

        if limit is not None:
            result = result[:limit]

        return result

    def create_pollution(self, pollution_data: List[Pollution]) -> None:
        self.pollutions.extend(pollution_data)

    def delete_pollution_range(self, start: date, end: date, city_id: int):
        temp = []
        begin_len = len(self.pollutions)
        for pollution in self.pollutions:
            if (
                pollution.date < start or pollution.date > end
            ) or city_id != pollution.city_id:
                temp.append(pollution)
        self.pollutions = temp
        end_len = len(self.pollutions)
        return begin_len - end_len

    def get_pollution_by_id(self, pollution_id: int) -> Any:
        return self.db.query(Pollution).get(pollution_id)

    def update_pollution(
        self, pollution_id: int, pollution_data: Dict[Any, Any]
    ) -> Optional[Pollution]:
        for pollution in self.pollutions:
            if pollution.id == pollution_data.get(pollution.id):
                pollution.co = pollution_data.get("co")
                pollution.no = pollution_data.get("no")
                pollution.no2 = pollution_data.get("no2")
                pollution.o3 = pollution_data.get("o3")
                pollution.so2 = pollution_data.get("so2")
                pollution.pm2_5 = pollution_data.get("pm2_5")
                pollution.pm10 = pollution_data.get("pm10")
                pollution.nh3 = pollution_data.get("nh3")
                return pollution
        return None
