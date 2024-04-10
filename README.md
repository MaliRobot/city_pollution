# City Pollution API

## API to get the latest or historical pollution data on your own or any other city on the planet!

- Identify any city of interest by the coordinates and the name (this way avoids confusion) and import data to the
  system for the desired period
- You can look up any city you want
- Get the data for any period and city already imported in daily periods, but you can also aggregate it by monthly or
  yearly periods
- If you need to for any reason, you can always delete or reimport data

## Built with

- ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
- ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
- ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)

## Instructions

### Get keys for external services

- Obtain API key from [Opencagedata](https://opencagedata.com/api), which is needed so the app can look up for city by
  the name and by the geocoordinates (reverse lookup). The city can only be reasonably identified once both the name and
  the coordinates lookup produce a good match.
- Register an account and obtain an API key from [Openweather](https://openweathermap.org/api) - that's where we are
  getting air pollution data from! Data is obtained by using coordinates so that's why we need them in the first step.
  You don't need a subscription for this.

### Setup

- Fill up .env file with your keys and db connection parameters
- Install Python and Poetry. Run:
   ```python
   poetry install
   ```
- Assuming you have installed Postgres locally, create a database, and run alembic to apply migrations:
  ```python
  alembic upgrade head
  ```

Alternatively, just run it from Docker:

```shell
docker compose build
docker compose up
```

You are all set, check endpoints at `/docs`

## How to

- Start with `api/city/name` - just type the name of your city, a native or English name will suffice.
- Check the response, if you find the city you are looking for, you can tell because country, state, and
  other data will help you, take the longitude and latitude.
- To get the data for your city, use `api/pollution` and send in the body longitude, latitude, and city name, as well as
  a desired date range.
- Now you can access data via GET `api/pollution` providing city name and date range as query params.
- List can be aggregated by month or year, and if any gaps are detected in the data, it will be indicated by the `gaps`
  flag.
- The rest is up to you. You can import more data for your city or other cities, you can delete pollution data
  and city data (the latter will delete pollution data as well).
