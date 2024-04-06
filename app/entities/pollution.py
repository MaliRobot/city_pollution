from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class Pollution:
    co: str
    no: str
    no2: str
    o3: float
    pm2_5: float
    pm10: str
    nh3: str
    timestamp: int
    site_id: Optional[int]
    id: Optional[int] = None


def pollution_factory(data: Dict[Any, Any], city_id: int) -> Pollution:
    components = data["components"]
    return Pollution(
        co=components["co"],
        no=components["no"],
        no2=components["no2"],
        o3=components["o3"],
        pm2_5=components["pm2_5"],
        pm10=components["pm10"],
        nh3=components["nh3"],
        timestamp=data["dt"],
        site_id=city_id,
    )
