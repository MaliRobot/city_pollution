import httpx


def test_get_city_coords_by_name() -> None:
    valid_name = "New York"
    response = httpx.get(
        "http://localhost:8000/api/city/name/", params={"name": valid_name}
    )
    assert response.status_code == 200
    data = response.json()

    response = httpx.get("http://localhost:8000/api/city/name/", params={"name": ""})
    assert response.status_code == 422

    long_name = "a" * 256
    response = httpx.get(
        "http://localhost:8000/api/city/name/", params={"name": long_name}
    )
    assert response.status_code == 422
