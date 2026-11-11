from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):

    APP_NAME: str = "Knowledge Atlas"
    APP_ENV: str = "development"

    DATABASE_URL: str

    SECRET_KEY: str

    UPLOAD_DIR: Path = BASE_DIR / "storage" / "uploads"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()