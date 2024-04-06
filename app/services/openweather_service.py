from typing import List, Dict, Any

from fastapi import HTTPException
from httpx import AsyncClient

from app.config.settings import settings


async def get_pollution_data(
    lat: float, lon: float, start: int, end: int
) -> List[Dict[str, Any]]:
    async with AsyncClient() as client:
        response = await client.get(
            f"{settings.openweather_url}?lat={lat}&lon={lon}&start={start}&end={end}&appid={settings.openweather_key}"
        )

    if response.status_code == 200:
        if response.status_code == 200:
            pollutions_list = []
            if len(response.json()["list"]) > 0:
                pollutions = response.json()["list"]
                for pollution in pollutions:
                    d = pollution["components"]
                    d["timestamp"] = pollution["dt"]
                    pollutions_list.append(d)
                return pollutions_list
        return []
    raise HTTPException(
        status_code=response.status_code, detail="Couldn't retrieve pollution data"
    )
