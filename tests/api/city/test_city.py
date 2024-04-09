from pytest_mock import MockerFixture

from data_project.tests.config import client


def test_get_city_coords_by_name(
        mock_city_repository_for_city_router, mocker: MockerFixture
) -> None:
    valid_name = "New York"
    response = client.get("api/city/name/", params={"name": valid_name})
    assert response.status_code == 200
    data = response.json()

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
