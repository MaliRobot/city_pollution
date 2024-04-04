from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    fastapi_env: str = ""
    database_url: str = ""
    db_name: str = ""
    db_user: str = ""
    db_host: str = ""
    db_password: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
