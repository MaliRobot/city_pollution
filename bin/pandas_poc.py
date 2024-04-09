from typing import List

import pandas as pd
from httpx import AsyncClient
from pandas import DataFrame

from data_project.config.settings import settings
from data_project.entities import Pollution


#
# async def get_cities(lat: float, lon: float, name: str) -> Optional[City]:
#     geocoder = await get_geocoder()
#     locs_by_reverse = geocoder.reverse_geocode(lat, lon)
#     all_locations = [
#         city_factory(loc)
#         for loc in locs_by_reverse
#         if loc["components"]["_type"] in ["city", "town"]
#     ]
#     if not all_locations:
#         locations_by_name = await get_city_by_name(name)
#         cities = [
#             city_factory(loc)
#             for loc in locations_by_name
#             if loc["components"]["_type"] in ["city", "town"]
#         ]
#         for city in cities:
#             if (
#                     city is not None
#                     and abs(city.lat - lat) < 0.5
#                     and abs(city.lon - lon) < 0.5
#             ):
#                 return city
#     return None


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
                d = pollution["components"]
                d["timestamp"] = pollution["dt"]
                pollutions_list.append(d)

            df = DataFrame(pollutions_list)
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")

            # Convert 'timestamp' column to separate date and time columns
            df["date"] = df["timestamp"].dt.date

            # get float columns
            float_columns = df.select_dtypes(include=["float"]).columns

            # fill the missing values with mean values
            df[float_columns] = df[float_columns].fillna(df[float_columns].mean())

            # group by date and calculate mean values
            df_daily_mean = df.groupby("date").mean()

            # round float values to 2 decimals
            df_daily_mean = df_daily_mean.round(2)

            df_daily_mean["city_id"] = city_id

            dataclass_instances = []
            for index, row in df_daily_mean.iterrows():
                instance = Pollution(
                    co=row["co"],
                    no=row["no"],
                    no2=row["no2"],
                    o3=row["o3"],
                    so2=row["so2"],
                    pm2_5=row["pm2_5"],
                    pm10=row["pm10"],
                    nh3=row["nh3"],
                    date=index,
                    city_id=city_id,
                )
                dataclass_instances.append(instance)
        return dataclass_instances
    return None


async def test_fetch_pollution_by_coords():
    r = await fetch_pollution_by_coords(
        lat=45, lon=20, start=1711296800, end=1712296800, city_id=1
    )


import asyncio

asyncio.run(test_fetch_pollution_by_coords())
