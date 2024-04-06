from dataclasses import dataclass
from datetime import date
from typing import List, Optional, Dict, Any, Type

from sqlalchemy import and_

from app.dependencies import Session
from app.entities.pollution import Pollution


@dataclass
class PollutionRepository:
    db: Session

    def create_pollution(self, pollution_data: List[Pollution]) -> None:
        self.db.bulk_save_objects(pollution_data)
        self.db.commit()

    def get_pollution_by_id(self, pollution_id: int) -> Any:
        return self.db.query(Pollution).get(pollution_id)

    def get_pollution(
        self, start: date, end: date, city_id: int
    ) -> list[Type[Pollution]]:
        return (
            self.db.query(Pollution)
            .filter(
                Pollution.city_id == city_id,
                and_(
                    Pollution.date >= start,
                    Pollution.date <= end,
                ),
            )
            .all()
        )

    def update_pollution(
        self, pollution_id: int, pollution_data: Dict[Any, Any]
    ) -> Optional[Pollution]:
        pollution = self.get_pollution_by_id(pollution_id)
        if pollution:
            for key, value in pollution_data:
                setattr(pollution, key, value)
            self.db.commit()
            self.db.refresh(pollution)
        return pollution

    def delete_pollution_range(self, start: date, end: date, city_id: int) -> int:
        result = (
            self.db.query(Pollution).filter(
                Pollution.date >= start,
                Pollution.date <= end,
                Pollution.city_id == city_id,
            )
        ).delete()

        self.db.commit()
        return result if result is not None else 0

    def get_all_pollution(self) -> list[Type[Pollution]]:
        return self.db.query(Pollution).all()
