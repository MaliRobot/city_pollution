from typing import List, Dict

import pandas as pd
from pandas import DataFrame

from app.entities import Pollution
from app.services.openweather_service import get_pollution_data


async def fetch_pollution_by_coords(
    lat: float,
    lon: float,
    start: int,
    end: int,
    city_id: int,
) -> List[Pollution] | None:
    pollution_data_list = await get_pollution_data(lat, lon, start, end)
    if pollution_data_list is None:
        return None
    return await pollution_to_dataframe(pollution_data_list, city_id)


async def pollution_to_dataframe(
    pollution_data_list: List[Dict], city_id: int
) -> List[Pollution]:
    df = DataFrame(pollution_data_list)
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")

    # convert timestamp to new date column
    df["date"] = df["timestamp"].dt.date

    # get float columns
    float_columns = df.select_dtypes(include=["float"]).columns

    # fill the missing values with mean values
    df[float_columns] = df[float_columns].fillna(df[float_columns].mean())

    # group by date and calculate mean values
    df_daily_mean = df.groupby("date").mean()

    # round float values to 2 decimals
    df_daily_mean = df_daily_mean.round(2)

    pollutions = []
    for index, row in df_daily_mean.iterrows():
        pollution = Pollution(
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
        pollutions.append(pollution)
    return pollutions
