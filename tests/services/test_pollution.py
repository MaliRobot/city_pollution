from dataclasses import asdict
from datetime import date, datetime

import pytest

from city_pollution.entities.pollution import Pollution
from city_pollution.schemas.pollution import Aggregate
from city_pollution.services.pollution import (
    pollution_to_dataframe,
    aggregated_pollutions,
)
from tests.repositories.pollution import PollutionFactory


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

    start = 1704104579  # 1st of Jan 2024
    city_id = 1
    pollutions_list = []
    for i in range(31):  # till 1st of April 2024
        start_date = datetime.fromtimestamp(start).date()
        pollution = PollutionFactory().create(start_date, city_id)
        poll_dict = asdict(pollution)
        poll_dict["timestamp"] = datetime.combine(
            poll_dict["date"], datetime.min.time()
        )
        pollutions_list.append(poll_dict)
        start += 3600 * 24  # day
    result = await pollution_to_dataframe(pollutions_list, 1)
    assert len(result) == 31


@pytest.mark.asyncio
async def test_aggr_pollution_to_dataframe():
    # test monthly
    start = 1704104579  # 1st of Jan 2024
    city_id = 1
    pollutions_list = []
    for i in range(91):  # till 1st of April 2024
        start_date = datetime.fromtimestamp(start).date()
        pollution = PollutionFactory().create(start_date, city_id)
        pollutions_list.append(pollution)
        start += 3600 * 24  # day

    result, gaps = aggregated_pollutions(
        pollutions_list, city_id, Aggregate.MONTHLY.value
    )

    assert gaps == False
    assert len(result) == 3
    first_dt = result[0].date.to_pydatetime()
    last_dt = result[-1].date.to_pydatetime()
    first_dt = first_dt.date()
    last_dt = last_dt.date()
    assert first_dt == date(2024, 1, 1)
    assert last_dt == date(2024, 3, 1)

    pollutions_list_w_gaps = pollutions_list[:2] + pollutions_list[5:]
    result, gaps = aggregated_pollutions(
        pollutions_list_w_gaps, city_id, Aggregate.MONTHLY.value
    )

    assert gaps == True
    assert len(result) == 3
    first_dt = result[0].date.to_pydatetime()
    last_dt = result[-1].date.to_pydatetime()
    first_dt = first_dt.date()
    last_dt = last_dt.date()
    assert first_dt == date(2024, 1, 1)
    assert last_dt == date(2024, 3, 1)

    # test yearly
    pollutions_list = []
    start = 1609459200  # 1st of Jan 2021
    for i in range(1094):  # days beetween 1st of Jan 2021 to 1st of Jan 2024
        start_date = datetime.fromtimestamp(start).date()
        pollution = PollutionFactory().create(start_date, city_id)
        pollutions_list.append(pollution)
        start += 3600 * 24  # day

    result, gaps = aggregated_pollutions(
        pollutions_list, city_id, Aggregate.YEARLY.value
    )

    assert gaps == False
    assert len(result) == 3
    first_dt = result[0].date.to_pydatetime()
    last_dt = result[-1].date.to_pydatetime()
    first_dt = first_dt.date()
    last_dt = last_dt.date()
    assert first_dt == date(2021, 1, 1)
    assert last_dt == date(2023, 1, 1)

    # test yearly with gaps
    pollutions_list = []
    start = 1609459200  # 1st of Jan 2021
    for i in range(1094):  # days beetween 1st of Jan 2021 to 1st of Jan 2024
        start_date = datetime.fromtimestamp(start).date()
        pollution = PollutionFactory().create(start_date, city_id)
        pollutions_list.append(pollution)
        start += 3600 * 24  # day

    pollutions_list_w_gaps = pollutions_list[:24] + pollutions_list[55:]
    result, gaps = aggregated_pollutions(
        pollutions_list_w_gaps, city_id, Aggregate.YEARLY.value
    )

    # test yearly with gaps
    assert gaps == True
    assert len(result) == 3
    first_dt = result[0].date.to_pydatetime()
    last_dt = result[-1].date.to_pydatetime()
    first_dt = first_dt.date()
    last_dt = last_dt.date()
    assert first_dt == date(2021, 1, 1)
    assert last_dt == date(2023, 1, 1)
