from pytest_mock import MockerFixture

from city_pollution.entities import City
from tests.config import client


def test_get_city_coords_by_name(
        mock_city_repository_for_city_router, mocker: MockerFixture
) -> None:
    async def get_fake_city_by_name(city_name: str) -> City:
        return City(
            id=1,
            name="New York",
            country="US",
            state="New York",
            county="New York",
            lat=45.45,
            lon=45.45,
        )

    mocker.patch("city_pollution.routers.city.get_city_by_name", get_fake_city_by_name)

    valid_name = "New York"
    response = client.get("api/city/name/", params={"name": valid_name})
    assert response.status_code == 200

    response = client.get("api/city/name/", params={"name": ""})
    assert response.status_code == 422

    long_name = "a" * 256
    response = client.get("api/city/name/", params={"name": long_name})
    assert response.status_code == 422


def test_delete_city_by_id_success(mock_city_repository_for_city_router) -> None:
    response = client.delete("api/city/1/")
    assert response.status_code == 200
    assert response.json() == {"message": "City deleted successfully"}


def test_delete_city_by_id_failure(mock_city_repository_for_city_router) -> None:
    response = client.delete("api/city/999/")
    assert response.status_code == 404
    assert response.json() == {"detail": "Delete failed, city not found"}
