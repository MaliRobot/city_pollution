from sqlalchemy import Table, Column, Integer, Float, ForeignKey, Date

from .base import mapper_registry

pollution_table = Table(
    "pollution",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("co", Float, nullable=False),
    Column("no", Float, nullable=False),
    Column("no2", Float, nullable=False),
    Column("o3", Float, nullable=False),
    Column("so2", Float),
    Column("pm2_5", Float),
    Column("pm10", Float),
    Column("nh3", Float),
    Column("date", Date),
    Column("city_id", ForeignKey("city.id", ondelete="CASCADE"), index=True),
)
