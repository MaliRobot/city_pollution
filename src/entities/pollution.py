from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Pollution:
    co: float
    no: float
    no2: float
    o3: float
    so2: float
    pm2_5: float
    pm10: float
    nh3: float
    date: date
    city_id: Optional[int]
    id: Optional[int] = None
