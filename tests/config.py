from fastapi.testclient import TestClient

from app.dependencies import get_db
from app.main import app


class FakeDB:
    def add(self, object):
        return object

    def commit(self):
        return

    def rollback(self):
        return

    def refresh(self, instance):
        return

    def flush(self):
        return


def override_get_db(fake_db=None):
    return fake_db


# Unit tests not to use the database - mocking instead.
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)
