from dataclasses import dataclass
from typing import List, Optional

from app.dependencies import Session
from app.entities.pollution import Pollution


@dataclass
class PollutionRepository:
    db: Session

    def create_pollution(self, pollution_data: List) -> None:
        self.db.bulk_save_objects(pollution_data)
        self.db.commit()

    def get_pollution_by_id(self, pollution_id: int) -> Optional[Pollution]:
        return self.db.query(Pollution).get(pollution_id)

    def update_pollution(
            self, pollution_id: int, pollution_data: dict
    ) -> Optional[Pollution]:
        pollution = self.get_pollution_by_id(pollution_id)
        if pollution:
            for key, value in pollution_data.items():
                setattr(pollution, key, value)
            self.db.commit()
            self.db.refresh(pollution)
        return pollution

    def delete_pollution(self, pollution_id: int) -> None:
        pollution = self.get_pollution_by_id(pollution_id)
        if pollution:
            self.db.delete(pollution)
            self.db.commit()

    def get_all_pollution(self) -> list[Pollution]:
        return self.db.query(Pollution).all()
