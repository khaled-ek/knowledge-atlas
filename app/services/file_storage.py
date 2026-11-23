
import uuid

from pathlib import Path

from fastapi import UploadFile

from app.core.config import settings

class FileStorageService:

    @staticmethod
    def ensure_upload_directory() -> None:
        settings.UPLOAD_DIRECTORY.mkdir(
            parents=True,
            exist_ok=True
        )

    @staticmethod
    async def save_file(file: UploadFile) -> tuple[str, int]:

        FileStorageService.ensure_upload_directory()

        file_extension = Path(file.filename or "").suffix.lower()

        unique_file_name = f"{uuid.uuid4()}{file_extension}"

        file_path = settings.UPLOAD_DIRECTORY / unique_file_name

        file_size = 0

        try:
            with file_path.open(mode="wb") as destination:
                while chunk := await file.read(settings.FILE_READ_CHUNK_SIZE):
                    file_size += len(chunk)
                    destination.write(chunk)

        except Exception:
            if file_path.exists():
                file_path.unlink()
            raise

        finally:
            await file.close()

        return unique_file_name, file_size

    @staticmethod
    def delete_file(storage_key: str) -> None:

        file_path = settings.UPLOAD_DIRECTORY / storage_key

        if file_path.exists() and file_path.is_file():
            file_path.unlink()

