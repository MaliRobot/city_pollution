from dataclasses import dataclass
from typing import Optional, Dict


@dataclass
class City:
    name: str
    state: str
    country: str
    lat: float
    lon: float
    county: str = None
    id: Optional[int] = None

    @staticmethod
    def from_raw_data(raw_data: Dict) -> Optional["City"]:
        data = raw_data["components"]
        if data["_type"] == "city":
            city_name = data.get("city") or data.get("town")
            if not city_name:
                return None
            city = City(
                name=city_name,
                state=data["state"],
                country=data["country"],
                lat=raw_data["geometry"]["lat"],
                lon=raw_data["geometry"]["lng"],
            )
            if "county" in data.keys():
                city.country = data.get("county", city.country)
            return city
        return None
