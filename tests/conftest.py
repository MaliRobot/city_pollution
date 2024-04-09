import pytest

from tests.config import override_get_db, app, get_db, FakeDB

pytest_plugins = ["tests.api.city.fixtures", "tests.api.pollution.fixtures"]


@pytest.fixture
def fake_repo() -> None:
    fake_db = FakeDB
    fake_db = override_get_db(fake_db)
    app.dependency_overrides[get_db] = fake_db
    yield
