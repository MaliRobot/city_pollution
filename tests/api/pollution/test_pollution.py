from datetime import datetime

import httpx


def test_valid_pollution_params(mocker) -> None:
    valid_params = {
        "lat": 40.7128,
        "lon": -74.0060,
        "start": datetime(2024, 1, 1).date(),
        "end": datetime(2024, 1, 2).date(),
    }

    response = httpx.get("http://localhost:8000/api/pollution/", params=valid_params)
    assert response.status_code == 200


def test_invalid_start_timestamp() -> None:
    invalid_start = {
        "lat": 40.7128,
        "lon": -74.0060,
        "start": datetime(2024, 2, 1).date(),
        "end": datetime(2024, 1, 2).date(),
    }
    response = httpx.get("http://localhost:8000/api/pollution/", params=invalid_start)
    assert response.status_code == 422


def test_invalid_end_timestamp() -> None:
    invalid_end = {
        "lat": 40.7128,
        "lon": -74.0060,
        "start": datetime(2024, 1, 1).date(),
        "end": datetime(2999, 1, 2).date(),
        "name": "New City",
    }
    response = httpx.get("http://localhost:8000/api/pollution/", params=invalid_end)
    assert response.status_code == 422

    invalid_end["end"] = invalid_end["start"] - 10000
    response = httpx.get("http://localhost:8000/api/pollution/", params=invalid_end)
    assert response.status_code == 422


def test_import_pollution_data() -> None:
    pollution_payload = {
        "lat": 40.7128,
        "lon": -74.0060,
        "start": datetime(2024, 1, 1).date(),
        "end": datetime(2024, 2, 1).date(),
        "name": "New City",
    }
    response = httpx.post(
        "http://localhost:8000/api/pollution/", json=pollution_payload
    )
    assert response.status_code == 200


def test_delete_pollution_data() -> None:
    query_params = {
        "lat": 40.7128,
        "lon": -74.0060,
        "start": datetime(2024, 1, 1).date(),
        "end": datetime(2024, 2, 1).date(),
        "name": "New City",
    }
    response = httpx.delete("http://localhost:8000/api/pollution/", params=query_params)
    assert response.status_code == 200
