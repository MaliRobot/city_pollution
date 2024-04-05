from datetime import datetime

import httpx


def test_valid_pollution_params():
    valid_params = {
        "lat": 40.7128,
        "lon": -74.0060,
        "start": int(datetime(2022, 1, 1).timestamp()),
        "end": int(datetime(2022, 1, 2).timestamp()),
    }
    response = httpx.get("http://localhost:8000/api/pollution/", params=valid_params)
    assert response.status_code == 200


def test_invalid_start_timestamp():
    invalid_start = {
        "lat": 40.7128,
        "lon": -74.0060,
        "start": -1,
        "end": int(datetime(2022, 1, 2).timestamp()),
    }
    response = httpx.get("http://localhost:8000/api/pollution/", params=invalid_start)
    assert response.status_code == 422


def test_invalid_end_timestamp():
    invalid_end = {
        "lat": 40.7128,
        "lon": -74.0060,
        "start": int(datetime(2022, 1, 1).timestamp()),
        "end": int(datetime.now().timestamp())
               + 3600,  # set end timestamp to 1 hour in the future
        "name": "New City",
    }
    response = httpx.get("http://localhost:8000/api/pollution/", params=invalid_end)
    assert response.status_code == 422

    invalid_end["end"] = invalid_end["start"] - 10000
    response = httpx.get("http://localhost:8000/api/pollution/", params=invalid_end)
    assert response.status_code == 422


def test_import_pollution_data():
    pollution_payload = {
        "lat": 40.7128,
        "lon": -74.0060,
        "start": 1649347200,
        "end": 1649433600,
        "name": "New City",
    }
    response = httpx.post(
        "http://localhost:8000/api/pollution/", json=pollution_payload
    )
    assert response.status_code == 200


def test_delete_pollution_data():
    query_params = {
        "lat": 40.7128,
        "lon": -74.0060,
        "start": 1649347200,
        "end": 1649433600,
        "name": "New City",
    }
    response = httpx.delete("http://localhost:8000/api/pollution/", params=query_params)
    assert response.status_code == 200
