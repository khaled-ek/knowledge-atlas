
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.source import Source


class SourceRepository:

    @staticmethod
    def get_source_by_id(
        db: Session,
        source_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> Source | None:

        statement = select(Source).where(
            Source.id == source_id,
            Source.user_id == user_id,
        )

        return db.scalar(statement)

    @staticmethod
    def get_sources_by_user(
        db: Session,
        user_id: uuid.UUID,
    ) -> list[Source]:

        statement = (
            select(Source)
            .where(Source.user_id == user_id)
            .order_by(Source.created_at.desc())
        )

        return list(db.scalars(statement).all())

    @staticmethod
    def create_source(
        db: Session,
        user_id: uuid.UUID,
        original_file: str,
        storage_key: str,
        file_type: str,
        file_size_bytes: int,
        status: str = "pending",
    ) -> Source:

        new_source = Source(
            user_id=user_id,
            original_file=original_file,
            storage_key=storage_key,
            file_type=file_type,
            file_size_bytes=file_size_bytes,
            status=status,
        )

        db.add(new_source)
        db.commit()
        db.refresh(new_source)

        return new_source

    @staticmethod
    def delete_source(
        db: Session,
        source: Source,
    ) -> None:

        db.delete(source)
        db.commit()
