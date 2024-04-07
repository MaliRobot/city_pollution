from dataclasses import dataclass
from typing import Optional


@dataclass
class City:
    id: Optional[int]
    name: str
    state: str
    country: str
    lat: float
    lon: float
    time_created: Optional[int] = None
    county: Optional[str] = None


__all__ = ["City"]
