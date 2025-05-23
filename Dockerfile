FROM python:3.12-alpine as base

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

RUN apk update && \
    apk add libpq postgresql-client  # <-- add postgresql-client here

FROM base as builder

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

RUN apk update && \
    apk add musl-dev build-base gcc gfortran openblas-dev curl postgresql-client  # <-- and here

WORKDIR /app

# Install Poetry
RUN pip install poetry==1.8.2

# Install the app
COPY pyproject.toml poetry.lock ./
RUN poetry install

FROM base as runtime

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

WORKDIR /app

COPY city_pollution ./city_pollution
COPY ./alembic.ini ./alembic.ini
COPY ./entrypoint.sh ./entrypoint.sh

RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
