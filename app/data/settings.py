from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "Birdhub"
    database_url: str = "sqlite:///./sql_app.db"
    model_config = SettingsConfigDict(env_file=".env")
    upload_folder: str = "uploads"


@lru_cache
def get_settings():
    return Settings()


def get_settings_test(upload_folder=None):
    if upload_folder is not None:
        return Settings(
            app_name="Birdhub (test)",
            database_url="sqlite://",
            upload_folder=upload_folder,
        )
    return Settings(app_name="Birdhub (test)", database_url="sqlite://")
