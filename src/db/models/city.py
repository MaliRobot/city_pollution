from datetime import datetime

from sqlalchemy import Table, Column, Integer, String, Float, UniqueConstraint

from .base import mapper_registry

city_table = Table(
    "city",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255), nullable=False, index=True),
    Column("state", String(255), nullable=False),
    Column("country", String(255), nullable=False),
    Column("county", String(255)),
    Column("lat", Float, nullable=False),
    Column("lon", Float, nullable=False),
    Column("time_created", Integer, default=datetime.now().timestamp()),
    Column("time_updated", Integer),
    UniqueConstraint("name", "lat", "lon"),
)
