from datetime import date

import pytest

from data_project.entities.pollution import Pollution
from data_project.services.pollution import pollution_to_dataframe


@pytest.mark.asyncio
async def test_pollution_to_dataframe():
    pollution_data_list = [
        {
            "co": 100,
            "no": 0,
            "no2": 10,
            "o3": 20,
            "so2": 5,
            "pm2_5": 22,
            "pm10": 1,
            "nh3": 0,
            "timestamp": 1712264400,
        },
        {
            "co": 100,
            "no": 0,
            "no2": 12,
            "o3": 30,
            "so2": 10,
            "pm2_5": 44,
            "pm10": 1,
            "nh3": 1,
            "timestamp": 1712268000,
        },
    ]
    city_id = 1

    pollutions = await pollution_to_dataframe(pollution_data_list, city_id)

    date_data = date(2024, 4, 4)
    expected_pollutions = [
        Pollution(
            co=100,
            no=0.0,
            no2=11.0,
            o3=25.0,
            so2=7.5,
            pm2_5=33.0,
            pm10=1.0,
            nh3=0.5,
            date=date_data,
            city_id=city_id,
        ),
    ]
    assert pollutions == expected_pollutions
