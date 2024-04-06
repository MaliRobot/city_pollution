from typing import Dict, List

from httpx import AsyncClient

from app.config.settings import settings
from app.entities import Pollution


async def fetch_pollution_by_coords(
    lat: float,
    lon: float,
    start: int,
    end: int,
) -> List[Pollution] | None:
    async with AsyncClient() as client:
        response = await client.get(
            f"{settings.openweather_url}?lat={lat}&lon={lon}&start={start}&end={end}&appid={settings.openweather_key}"
        )
    if response.status_code == 200:
        pollutions_list = []
        if len(response.json()["list"]) > 0:
            pollutions = response.json()["list"]
            for pollution in pollutions:
                pollution = Pollution.from_raw_data(pollution)
                pollutions_list.append(pollution)
        return pollutions_list
    return None


async def update_pollution(lat: float, lon: float, start: int, end: int) -> Dict:
    raise NotImplemented


async def get_pollution_by_coords(lat: float, lon: float, start: int, end: int) -> Dict:
    raise NotImplemented


async def delete_pollution_by_coords(
    lat: float, lon: float, start: int, end: int
) -> Dict:
    raise NotImplemented
