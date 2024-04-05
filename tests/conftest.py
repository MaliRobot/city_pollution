import pytest

from tests.config import override_get_db, app, get_db, FakeDB

pytest_plugins = []


@pytest.fixture
def fake_repo():
    fake_db = FakeDB
    fake_db = override_get_db(fake_db)
    app.dependency_overrides[get_db] = fake_db
    yield
