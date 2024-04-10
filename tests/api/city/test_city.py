from typing import Dict, Any, List

from pytest_mock import MockerFixture

from tests.config import client


def test_get_city_coords_by_name(
    mock_city_repository_for_city_router, mocker: MockerFixture
) -> None:
    async def get_fake_city_by_name(city_name: str) -> List[Dict[str, Any]]:
        return [
            {
                "components": {
                    "_category": "building",
                    "_normalized_city": "Hanover",
                    "_type": "building",
                    "city": "Hanover",
                    "city_district": "Vahrenwald-List",
                    "continent": "Europe",
                    "country": "Germany",
                    "country_code": "de",
                    "county": "Region Hannover",
                    "house_number": "2",
                    "office": "Design Offices",
                    "political_union": "European Union",
                    "postcode": "30165",
                    "road": "Philipsbornstraße",
                    "state": "Lower Saxony",
                    "state_code": "NI",
                    "suburb": "Vahrenwald",
                },
                "geometry": {"lat": 52.387783, "lng": 9.7334394},
            }
        ]

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
