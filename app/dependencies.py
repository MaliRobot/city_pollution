from typing import Iterator

from opencage.geocoder import OpenCageGeocode
from sqlalchemy.orm import Session

from app.config.settings import settings
from app.db.connection import session_maker


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
