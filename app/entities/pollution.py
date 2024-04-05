from dataclasses import dataclass


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
    id: int = None

    @staticmethod
    def from_raw_data(data):
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
        )
