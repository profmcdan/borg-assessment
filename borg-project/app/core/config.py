from functools import lru_cache
import os

from dotenv import load_dotenv
from pydantic import BaseSettings, PostgresDsn

load_dotenv()


class Settings(BaseSettings):
    api_v1_prefix: str
    debug: bool
    project_name: str
    version: str
    description: str

    # Database
    database_url: PostgresDsn
    test_database_url: PostgresDsn
    redis_server: str
    redis_port: int
    redis_db: int


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    return settings


settings = Settings()
