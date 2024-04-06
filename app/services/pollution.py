from typing import List

from httpx import AsyncClient

from app.config.settings import settings
from app.entities import Pollution
from app.entities.pollution import pollution_factory


async def fetch_pollution_by_coords(
        lat: float,
        lon: float,
        start: int,
        end: int,
        city_id: int,
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
                pollution = pollution_factory(pollution, city_id)
                pollutions_list.append(pollution)
        return pollutions_list
    return None
