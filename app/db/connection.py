from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config.settings import settings

DATABASE_URL = settings.database_url

_session_maker = None


def session_maker() -> sessionmaker:
    global _session_maker
    if _session_maker is None:
        engine = create_engine(DATABASE_URL)
        _session_maker = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return _session_maker
