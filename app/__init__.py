from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class CronSettings(BaseSettings):
    DATABASE_URL: str
    model_config = SettingsConfigDict(env_file=".env")


class Settings(CronSettings):
    ADMIN_USERNAME: str
    ADMIN_PASSWORD_HASH: str
    USER_MANAGER_SECRET: str


@lru_cache
def get_cron_settings() -> CronSettings:
    return CronSettings()


@lru_cache
def get_settings() -> Settings:
    return Settings()
