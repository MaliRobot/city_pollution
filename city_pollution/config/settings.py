from pathlib import Path
from tempfile import gettempdir

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    fastapi_env: str = ""
    database_url: str = ""
    postgres_name: str = ""
    postgres_user: str = ""
    postgres_host: str = ""
    postgres_port: str = ""
    postgres_password: str = ""
    opencage_url: str = ""
    opencage_key: str = ""
    openweather_url: str = ""
    openweather_key: str = ""
    temp_dir: Path = Path(gettempdir()) / "city_pollution" / "plots"
    plots_url_base: str = "/api/plots"

    class Config:
        env_file = ".env"


settings = Settings()
