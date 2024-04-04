from typing import Iterator

from sqlalchemy.orm import Session

from app.db.connection import session_maker


def get_db() -> Iterator[Session]:
    _session_maker = session_maker()
    db = _session_maker()
    try:
        yield db
    finally:
        db.close()
