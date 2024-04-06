from fastapi.testclient import TestClient

from app.dependencies import get_db
from app.main import app


class FakeDB:
    def add(self, obj: object) -> object:
        return obj

    def commit(self) -> None:
        return

    def rollback(self) -> None:
        return

    def refresh(self, instance) -> None:
        return

    def flush(self) -> None:
        return


def override_get_db(fake_db=None) -> None:
    return fake_db


# Unit tests not to use the database - mocking instead.
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)
