import logging
import uuid
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

import pandas as pd
from matplotlib import pyplot as plt
from pandas import DataFrame

from city_pollution.config.settings import settings
from city_pollution.entities import Pollution, City
from city_pollution.schemas.pollution import Aggregate
from city_pollution.services.openweather_service import get_pollution_data
from datetime import datetime
from typing import Union

from city_pollution.db.repositories.city_repository import CityRepository
from city_pollution.db.repositories.pollution_repository import PollutionRepository
from city_pollution.dependencies import Session
from city_pollution.schemas.city import City as CitySchema
from city_pollution.schemas.pollution import (
    PollutionSchema,
    PollutionItemList,
    PollutionItem,
    Dates,
)
from city_pollution.services.city import get_city


async def fetch_pollution_by_coords(
    lat: float,
    lon: float,
    start: int,
    end: int,
    city_id: int,
) -> List[Pollution] | None:
    """
    Get pollution data for a given city, coordinates and time range
    :param lat: Latitude of the location of interest
    :type: float
    :param lon: Longitude of the location of interest
    :type: float
    :param start: Start timestamp
    :type: int
    :param end: End timestamp
    :type: int
    :param city_id: ID of the city from our database - need to assign it to pollution entities
    :type: int
    :return:
    """
    pollution_data_list = await get_pollution_data(lat, lon, start, end)
    if pollution_data_list is None:
        return None
    return await pollution_to_dataframe(pollution_data_list, city_id)


async def pollution_to_dataframe(
    pollution_data_list: List[Dict[Any, Any]], city_id: int
) -> List[Pollution]:
    """
    Process dictionaries with pollution data using dataframe
    to aggregate pollution by date, performing mean of every
    float column in the pollution, and instantiating rows
    as Pollution objects
    :param pollution_data_list: List with dictionaries with fetched pollution data from external service
    :type pollution_data_list: List[Dict]
    :param city_id: ID of the city we are interested in
    :type city_id: int
    :return: Pollution data
    :rtype: List[Pollution]
    """
    df = DataFrame(pollution_data_list)
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
    # convert timestamp to new date column
    df["date"] = df["timestamp"].dt.date

    # check gaps
    gaps = check_date_gaps(df)
    if gaps:
        start = df.head(1)["date"]
        end = df.tail(1)["date"]
        logging.info(
            f"Gaps in import data in range {start} to {end} for city_id {city_id}"
        )

    # get float columns
    float_columns = df.select_dtypes(include=["float"]).columns
    # fill the missing values with mean values
    df[float_columns] = df[float_columns].fillna(df[float_columns].mean())
    # group by date and calculate mean values
    df_daily_mean = df.groupby("date").mean()
    # round float values to 2 decimals
    df_daily_mean = df_daily_mean.round(2)

    # convert to date
    df_daily_mean.reset_index(inplace=True)
    df_daily_mean["date"] = pd.to_datetime(df_daily_mean["date"])
    df_daily_mean["date"] = df_daily_mean["date"].dt.date

    return pandas_to_dataclasses(df_daily_mean, city_id)


def aggregated_pollutions(
    pollution_data_list: List[Pollution], city_id: int, aggregate: Optional[str] = None
) -> Tuple[List[Pollution], bool]:
    """
    :param pollution_data_list: List with dictionaries with fetched pollution data from external service
    :type pollution_data_list: List[Dict]
    :param city_id: ID of the city we are interested in
    :type city_id: int
    :param aggregate: Value by which to aggregate the data
    :type aggregate: str, optional
    :return: Pollution data
    :rtype: List[Pollution]
    """
    if not pollution_data_list:
        return [], False

    df = pd.DataFrame(pollution_data_list)
    # convert date to datetime
    df["date"] = pd.to_datetime(df["date"])

    # check gaps
    gaps = check_date_gaps(df)

    # get all float columns
    float_columns = df.select_dtypes(include="float").columns

    if aggregate == Aggregate.MONTHLY.value:
        freq = "month"
        period = "M"
    else:
        freq = "year"
        period = "Y"

    # group by freq and calculate mean value for float columns
    df[freq] = df["date"].dt.to_period(period)
    aggregated_df = df.groupby(freq)[float_columns].mean().reset_index()
    # convert the period index to datetime format with the first day of each month/year
    aggregated_df["date"] = aggregated_df[freq].dt.to_timestamp()

    # drop intermediate freq column
    aggregated_df.drop(columns=[freq], inplace=True)

    return pandas_to_dataclasses(aggregated_df, city_id), gaps


def check_date_gaps(df: pd.DataFrame) -> bool:
    """
    Check if date gaps exist in Pollution data
    :param df: DataFrame with pollution data
    :type df: DataFrame
    :return: true if date gaps exist in Pollution, else false
    :rtype: bool
    """
    df_copy = df.copy()
    df_copy["gaps"] = df_copy["date"].sort_values().diff() > pd.to_timedelta("1 day")
    if df_copy["gaps"].sum() > 0:
        return True
    return False


def pandas_to_dataclasses(df: pd.DataFrame, city_id: int) -> List[Pollution]:
    """
    Exports dataframe rows to Pollution class instances
    :param df: Dataframe containing the pollution data
    :type df: pd.DataFrame
    :param city_id:
    :return: List of instantiated Pollution dataclasses
    :rtype: List[Pollution]
    """
    pollutions = []
    for index, row in df.iterrows():
        pollution = Pollution(
            co=row["co"],
            no=row["no"],
            no2=row["no2"],
            o3=row["o3"],
            so2=row["so2"],
            pm2_5=row["pm2_5"],
            pm10=row["pm10"],
            nh3=row["nh3"],
            date=row["date"],
            city_id=city_id,
        )
        pollutions.append(pollution)
    return pollutions


def generate_pollution_plot(
    pollution_data: List[Pollution], city: City
) -> Optional[str]:
    """
    Generate a plot for pollution data and return the file path

    :param pollution_data: List of Pollution instances
    :param city: City instance
    :return: URL to the generated plot or None if no data
    """
    if not pollution_data:
        return None

    # Extract dates and pollutant values
    dates = [p.date for p in pollution_data]
    pollutants = {
        "CO": [p.co for p in pollution_data],
        "NO": [p.no for p in pollution_data],
        "NO2": [p.no2 for p in pollution_data],
        "O3": [p.o3 for p in pollution_data],
        "SO2": [p.so2 for p in pollution_data],
        "PM2.5": [p.pm2_5 for p in pollution_data],
        "PM10": [p.pm10 for p in pollution_data],
        "NH3": [p.nh3 for p in pollution_data],
    }

    # Create a figure with multiple subplots for each pollutant
    fig, axes = plt.subplots(4, 2, figsize=(14, 16))
    fig.suptitle(
        f"Pollution Data for {city.name} ({dates[0]} to {dates[-1]})", fontsize=16
    )

    # Plot each pollutant on its own subplot
    for i, (pollutant, values) in enumerate(pollutants.items()):
        row, col = divmod(i, 2)
        ax = axes[row, col]

        # Filter out None values
        valid_data = [(d, v) for d, v in zip(dates, values) if v is not None]
        if valid_data:
            plot_dates, plot_values = zip(*valid_data)
            ax.plot(plot_dates, plot_values, marker="o", linestyle="-", markersize=4)
            ax.set_title(pollutant)
            ax.set_ylabel("Concentration")
            ax.grid(True)

            # Set x-axis labels to be readable
            if len(plot_dates) > 10:
                # Show fewer x-ticks if there are many dates
                step = max(1, len(plot_dates) // 10)
                ax.set_xticks(plot_dates[::step])

            ax.tick_params(axis="x", rotation=45)
        else:
            ax.text(
                0.5,
                0.5,
                f"No data for {pollutant}",
                horizontalalignment="center",
                verticalalignment="center",
                transform=ax.transAxes,
            )

    # Adjust layout
    plt.tight_layout(rect=(0.0, 0.0, 1.0, 0.96))

    # Create a directory for storing plots if it doesn't exist yet
    plots_dir: Path = Path(settings.temp_dir)
    plots_dir.mkdir(parents=True, exist_ok=True)

    # Generate a unique filename
    safe_city_name = city.name.replace(" ", "_")
    plot_filename = (
        f"{safe_city_name}_{dates[0]}_{dates[-1]}_{uuid.uuid4().hex[:8]}.png"
    )
    plot_path = plots_dir / plot_filename

    # Save the plot
    plt.savefig(plot_path)
    plt.close(fig)

    # Return the URL for accessing the plot
    return f"{settings.plots_url_base}/{plot_filename}"


async def pollution_response_handler(
    pollution: List[Pollution], city: City, gaps: bool = False
) -> PollutionItemList:
    start_dt = end_dt = None
    plot_url = None

    if len(pollution) > 0:
        start_dt = pollution[0].date
        end_dt = pollution[-1].date
        plot_url = generate_pollution_plot(pollution, city)

    return PollutionItemList(
        data=[PollutionItem.model_validate(x) for x in pollution],
        city=CitySchema.model_validate(city),
        start=start_dt,
        end=end_dt,
        gaps=gaps,
        plot_url=plot_url,
    )


async def get_pollution_data_service(
    aggregate: Aggregate,
    city_id: int,
    dates: Dates,
    db: Session,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> PollutionItemList:
    city_repo = CityRepository(db)
    city = city_repo.get_city_by_id(city_id)

    if city and city.id:
        pollution_repo = PollutionRepository(db)
        if aggregate != Aggregate.DAILY:
            pollutions = pollution_repo.get_pollution(dates.start, dates.end, city.id)
            agg_pollution, gaps = aggregated_pollutions(
                pollutions, city.id, aggregate.value
            )
            result = await pollution_response_handler(agg_pollution, city, gaps)
            return result

        pollution = pollution_repo.get_pollution(
            dates.start, dates.end, city.id, limit, offset
        )
        result = await pollution_response_handler(pollution, city)
        return result
    raise ValueError("City not found")


async def import_historical_pollution(
    pollution_params: PollutionSchema, db: Session
) -> Dict[str, str]:
    city_repo = CityRepository(db)
    if pollution_params.name:
        city = city_repo.search_city(
            pollution_params.name, pollution_params.lat, pollution_params.lon
        )
    else:
        city = city_repo.get_city_by_lat_and_lon(
            pollution_params.lat, pollution_params.lon
        )

    if city is None:
        city_data = await get_city(
            pollution_params.lat, pollution_params.lon, pollution_params.name
        )
        if city_data:
            city = city_repo.create_city(city_data)

    if city and city.id:
        start_ts = int(
            datetime.combine(
                pollution_params.dates.start, datetime.min.time()
            ).timestamp()
        )
        end_ts = int(
            datetime.combine(
                pollution_params.dates.end, datetime.min.time()
            ).timestamp()
        )
        pollution_repo = PollutionRepository(db)
        pollution_repo.delete_pollution_range(
            pollution_params.dates.start, pollution_params.dates.end, city.id
        )
        pollution_data = await fetch_pollution_by_coords(
            pollution_params.lat,
            pollution_params.lon,
            start_ts,
            end_ts,
            city.id,
        )

        if pollution_data:
            pollution_repo.create_pollution(pollution_data)
            return {
                "success": f"pollution data imported for city {city.name} at coords {city.lat} {city.lon}"
            }
        else:
            raise ValueError("Pollution data not found")
    else:
        raise ValueError("City not found")


async def delete_pollution_data_service(
    city_id: int,
    dates: Dates,
    db: Session,
) -> Dict[str, Union[bool, int]]:
    city_repo = CityRepository(db)
    city = city_repo.get_city_by_id(city_id)
    if city and city.id:
        pollution_repo = PollutionRepository(db)
        result = pollution_repo.delete_pollution_range(dates.start, dates.end, city.id)
        return {"success": True, "deleted": result}
    raise ValueError("City not found")
