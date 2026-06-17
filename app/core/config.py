from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    google_api_key: str = ""
    google_api_model: str = "gemini-3-flash-preview"
    loop_count: int = 1

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()