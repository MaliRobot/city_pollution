import pytest

from tests.repositories.city import CityRepositoryPrepopulated
from tests.repositories.pollution import PollutionRepositoryPrepopulated


@pytest.fixture
def mock_city_repository(mocker):
    mocker.patch(
        "app.routers.pollution.CityRepository",
        CityRepositoryPrepopulated,
    )


@pytest.fixture
def mock_pollution_repository(mocker):
    mocker.patch(
        "app.routers.pollution.PollutionRepository",
        PollutionRepositoryPrepopulated,
    )
