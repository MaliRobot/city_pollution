from datetime import datetime, date
from typing import List

from pytest_mock import MockerFixture

from app.entities import City, Pollution
from tests.config import client
from tests.repositories.city import CityRepositoryPrepopulated
from tests.repositories.pollution import PollutionRepositoryPrepopulated, PollutionFactory


def test_valid_pollution_params(mocker: MockerFixture) -> None:
    mocker.patch(
        "app.routers.pollution.PollutionRepository",
        PollutionRepositoryPrepopulated,
    )
    mocker.patch(
        "app.routers.pollution.CityRepository",
        CityRepositoryPrepopulated,
    )

    valid_params = {
        "lat": 40.53,
        "lon": -74.56,
        "start": date(2024, 1, 1),
        "end": date(2024, 1, 2),
    }

    response = client.get("api/pollution/", params=valid_params)

    assert response.status_code == 200
    data = response.json()
    assert data["city"]["lat"] == 40.53
    assert data["city"]["lon"] == -74.56
    assert data["city"]["name"] == "San Francisco"
    assert len(data["data"]) > 0
    # assert all pollution data is for the given city
    assert set([x["city_id"] for x in data["data"]]) == {data["city"]["id"]}


def test_valid_pollution_params_no_data(mocker: MockerFixture) -> None:
    mocker.patch(
        "app.routers.pollution.PollutionRepository",
        PollutionRepositoryPrepopulated,
    )
    mocker.patch(
        "app.routers.pollution.CityRepository",
        CityRepositoryPrepopulated,
    )

    valid_params = {
        "lat": 40.53,
        "lon": -74.56,
        "start": date(2023, 1, 1),
        "end": date(2023, 1, 2),
    }

    response = client.get("api/pollution/", params=valid_params)
    assert response.status_code == 200
    assert response.json()['city']["name"] == "San Francisco"
    assert len(response.json()["data"]) == 0


def test_get_pollution_invalid_start_timestamp() -> None:
    invalid_start = {
        "lat": 40.7128,
        "lon": -74.0060,
        "start": datetime(2024, 2, 1).date(),
        "end": datetime(2024, 1, 2).date(),
    }
    response = client.get("api/pollution/", params=invalid_start)
    assert response.status_code == 422
    assert response.json() == {'detail': 'End time must be greater than start time'}


def test_get_pollution_invalid_end_timestamp() -> None:
    invalid_end = {
        "lat": 40.7128,
        "lon": -74.0060,
        "start": date(2024, 1, 1),
        "end": date(2999, 1, 2),
        "name": "New City",
    }
    response = client.get("api/pollution/", params=invalid_end)
    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == 'Input should be less than or equal to 2024-04-07'

    invalid_end["end"] = date(1999, 1, 1)
    response = client.get("api/pollution/", params=invalid_end)
    assert response.status_code == 422
    assert response.json() == {'detail': 'End time must be greater than start time'}


def test_import_pollution_data(mocker: MockerFixture) -> None:
    mocker.patch(
        "app.routers.pollution.PollutionRepository",
        PollutionRepositoryPrepopulated,
    )
    mocker.patch(
        # "app.routers.pollution.CityRepository",
        "app.routers.pollution.CityRepository",
        CityRepositoryPrepopulated,
    )

    async def fake_get_city(lat: float, lon: float, name: str) -> City | None:
        return City(id=None, lat=lat, lon=lon, name=name, country="US", county="", state="California", time_created=0)

    mocker.patch(
        "app.routers.pollution.get_city",
        fake_get_city,
    )

    async def fetch_pollution_by_coords(lat: float, lon: float, start: int, end: int, city_id: int) -> List[Pollution]:
        pollutions = []
        p_date = start
        while True:
            d = datetime.fromtimestamp(p_date).date()
            pollution = PollutionFactory.create(d, city_id)
            p_date += 3600  # hour
            pollutions.append(pollution)
            if p_date >= end:
                break
        return pollutions

    mocker.patch(
        "app.routers.pollution.fetch_pollution_by_coords",
        fetch_pollution_by_coords,
    )

    # get pollution for city that is not in db yet
    pollution_payload = {
        "lat": 40.7128,
        "lon": -74.0060,
        "start": date(2024, 1, 1).strftime("%Y-%m-%d"),
        "end": date(2024, 2, 1).strftime("%Y-%m-%d"),
        "name": "New City",
    }
    response = client.post(
        "api/pollution/", json=pollution_payload
    )

    assert response.status_code == 200
    assert response.json() == {'success': 'pollution data imported for city New City at coords 40.7128 -74.006'}

    # get pollution for city that is already in db
    pollution_payload = {
        "lat": 40.53,
        "lon": -74.56,
        "start": date(2023, 1, 1).strftime("%Y-%m-%d"),
        "end": date(2023, 1, 2).strftime("%Y-%m-%d"),
        "name": "San Francisco",
    }
    response = client.post(
        "api/pollution/", json=pollution_payload
    )

    assert response.status_code == 200
    assert response.json() == {'success': 'pollution data imported for city San Francisco at coords 40.53 -74.56'}

    # get pollution for city that is already in db but pollution data couldn't be fetched
    async def fetch_pollution_by_coords(lat: float, lon: float, start: int, end: int, city_id: int) -> List:
        return []

    mocker.patch(
        "app.routers.pollution.fetch_pollution_by_coords",
        fetch_pollution_by_coords,
    )

    pollution_payload = {
        "lat": 40.53,
        "lon": -74.56,
        "start": date(2023, 3, 1).strftime("%Y-%m-%d"),
        "end": date(2023, 3, 2).strftime("%Y-%m-%d"),
        "name": "San Francisco",
    }
    response = client.post(
        "api/pollution/", json=pollution_payload
    )

    assert response.status_code == 404
    assert response.json() == {'detail': 'Pollution data not found'}


def test_delete_pollution_data(mocker: MockerFixture) -> None:
    mocker.patch(
        "app.routers.pollution.PollutionRepository",
        PollutionRepositoryPrepopulated,
    )
    mocker.patch(
        "app.routers.pollution.CityRepository",
        CityRepositoryPrepopulated,
    )

    query_params = {
        "lat": 40.53,
        "lon": -74.56,
        "start": date(2024, 1, 1),
        "end": date(2024, 1, 2),
        "name": "San Francisco"
    }

    response = client.delete("api/pollution/", params=query_params)
    assert response.status_code == 200
    assert response.json() == {"success": True, "deleted": 2}

    query_params = {
        "lat": 40.53,
        "lon": -74.56,
        "start": date(2024, 2, 1),
        "end": date(2024, 2, 2),
        "name": "San Francisco"
    }

    # test deleting non existing pollution data
    response = client.delete("api/pollution/", params=query_params)
    assert response.status_code == 200
    assert response.json()["deleted"] == 0
