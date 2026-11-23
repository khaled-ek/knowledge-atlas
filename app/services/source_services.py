
import uuid

from pathlib import Path

from fastapi import UploadFile, HTTPException, status

from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.source import Source
from app.repositories.source_repository import SourceRepository
from app.services.file_storage import FileStorageService

class SourceService:

    @staticmethod
    async def upload_source(
        db: Session,
        user_id: uuid.UUID,
        file: UploadFile
    ) -> Source:

        # 1. Validate filename
        original_file = Path(file.filename or "").name

        if not original_file:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A filename is required."
            )

        # 2. Validate file extension
        extension = Path(original_file).suffix.lower()

        if extension != ".pdf":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="only PDF files are supported."
            )

        # 3. Validate MIME type
        if file.content_type != "application/pdf":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file type, please upload a PDF."
            )

        # 4. Save the file
        storage_key, file_size = await FileStorageService.save_file(file)

        # 5. Validate file size
        max_size = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024

        if file_size == 0:
            FileStorageService.delete_file(storage_key)

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The uploaded file is empty"
            )

        if file_size > max_size:
            FileStorageService.delete_file(storage_key)

            raise HTTPException(
                status_code=status.HTTP_413_CONTENT_TOO_LARGE,
                detail="The uploaded file exceeds the 20 MB limit."
            )

        # 6. Create database record
        try:
            source = SourceRepository.create_source(
                db=db,
                user_id=user_id,
                original_file=original_file,
                storage_key=storage_key,
                file_type="application/pdf",
                file_size_bytes=file_size,
                status="pending"
            )
            return source

        except Exception:
            # Remove the physical file if the database insetion fails
            FileStorageService.delete_file(storage_key)
            raise


