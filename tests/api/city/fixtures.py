import pytest

from tests.repositories.city import CityRepositoryPrepopulated


@pytest.fixture
def mock_city_repository_for_city_router(mocker):
    mocker.patch(
        "data_project.routers.city.CityRepository",
        CityRepositoryPrepopulated,
    )
