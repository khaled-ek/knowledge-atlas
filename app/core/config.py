from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):

    APP_NAME: str = "Knowledge Atlas"
    APP_ENV: str = "development"

    DATABASE_URL: str

    SECRET_KEY: str

    OPEN_API_KEY: str

    EMBEDDING_MODEL: str = "text-embedding-3-small"

    UPLOAD_DIRECTORY: Path = BASE_DIR / "storage" / "uploads"

    MAX_UPLOAD_SIZE_MB: int = 20

    FILE_READ_CHUNK_SIZE: int = 1024 * 1024  # 1 MB

    CHUNK_SIZE: int = 500  # tokens
    CHUNK_OVERLAP: int = 75  # tokens

    ALLOWED_FILE_TYPES: list[str] = [
        "application/pdf"
    ]

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()