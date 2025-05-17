from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    fastapi_env: str = ""
    database_url: str = ""
    postgres_name: str = ""
    postgres_user: str = ""
    postgres_host: str = ""
    postgres_password: str = ""
    opencage_url: str = ""
    opencage_key: str = ""
    openweather_url: str = ""
    openweather_key: str = ""

    class Config:
        env_file = ".env"


settings: Settings = Settings()
