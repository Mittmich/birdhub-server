from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    app_name: str = "Birdhub"
    database_url: str = "sqlite:///./sql_app.db"
    model_config = SettingsConfigDict(env_file=".env")

@lru_cache
def get_settings():
    return Settings()