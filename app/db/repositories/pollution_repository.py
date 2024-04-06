from dataclasses import dataclass
from typing import List, Optional, Dict, Any

from app.dependencies import Session
from app.entities.city import City
from app.entities.pollution import Pollution


@dataclass
class PollutionRepository:
    db: Session

    def create_pollution(self, pollution_data: List[Pollution]) -> None:
        print(pollution_data)
        self.db.bulk_save_objects(pollution_data)
        self.db.commit()

    def get_pollution_by_id(self, pollution_id: int) -> Any:
        return self.db.query(Pollution).get(pollution_id)

    def get_pollution(self, start: int, end: int, site_id: int) -> List[Pollution]:
        return (
            self.db.query(Pollution)
            .filter(
                Pollution.site_id == site_id,
                Pollution.timestamp >= start,
                Pollution.timestamp <= end,
            )
            .join(City)
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

    def delete_pollution_range(self, start: int, end: int, site_id: int) -> int:
        result = (
            self.db.query(Pollution).filter(
                Pollution.timestamp >= start,
                Pollution.timestamp <= end,
                Pollution.site_id == site_id,
            )
        ).delete()
        print(result)
        self.db.commit()
        return result

    def get_all_pollution(self) -> list[Pollution]:
        return self.db.query(Pollution).all()
