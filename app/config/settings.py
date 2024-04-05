from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    fastapi_env: str = ""
    database_url: str = ""
    db_name: str = ""
    db_user: str = ""
    db_host: str = ""
    db_password: str = ""
    opencage_url: str = ""
    opencage_key: str = ""
    openweather_url: str = ""
    openweather_key: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
