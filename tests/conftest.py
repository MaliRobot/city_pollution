import pytest

from data_project.tests.config import override_get_db, app, get_db, FakeDB

pytest_plugins = ["data_project.tests.api.city.fixtures", "data_project.tests.api.pollution.fixtures"]


@pytest.fixture
def fake_repo() -> None:
    fake_db = FakeDB
    fake_db = override_get_db(fake_db)
    app.dependency_overrides[get_db] = fake_db
    yield
