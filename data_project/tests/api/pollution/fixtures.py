import pytest

from data_project.tests.repositories import CityRepositoryPrepopulated
from data_project.tests.repositories import PollutionRepositoryPrepopulated


@pytest.fixture
def mock_city_repository(mocker):
    mocker.patch(
        "data_project.routers.pollution.CityRepository",
        CityRepositoryPrepopulated,
    )


@pytest.fixture
def mock_pollution_repository(mocker):
    mocker.patch(
        "data_project.routers.pollution.PollutionRepository",
        PollutionRepositoryPrepopulated,
    )
