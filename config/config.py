from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    DB_NAME: str = "data"
    DB_USERNAME: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_HOST: str = "postgres:5432"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
