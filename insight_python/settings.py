from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    MEMCACHEDCLOUD_SERVERS: str
    FASTAPI_PRODUCTION: bool = False


settings = Settings()
