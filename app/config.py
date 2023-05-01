
from functools import lru_cache

from pydantic import BaseSettings


class AppSettings(BaseSettings):
    DATABASE_URI: str
    TEST_DATABASE_URI: str
    WEATHER_API_KEY: str



@lru_cache()
def get_app_settings() -> AppSettings:
    return AppSettings()
