from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_DIALECT: str
    DATABASE_HOSTNAME: str
    DATABASE_NAME: str
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    DATABASE_PORT: int
    DEBUG_MODE: bool
    DATABASE_OTRO: str

    class Config:
        env_file = ".env.dev"


@lru_cache
def get_settings():
    return Settings()