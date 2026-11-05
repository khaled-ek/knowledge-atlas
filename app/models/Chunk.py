import string
import uuid
from datetime import datetime, timezone

from DateTime import DateTime
from sqlalchemy import String, Boolean, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from pgvector.sqlalchemy import Vector

from app.db.base import Base
from app.models.source import Source

class Chunk(Base):
    __tablename__ = "document_chunks"

    id : Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    source_id : Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("sources.id"),
        nullable=False,
        index=True

    )

    chunk_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    content: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    page_number: Mapped[int] = mapped_column(
        Integer,
        nullable=True
    )

    start_offset: Mapped[int] = mapped_column(
        Integer,
        nullable=True
    )

    end_offset: Mapped[int] = mapped_column(
        Integer,
        nullable=True
    )

    doc_metadata: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict
    )

    embedding: Mapped[list[float]] = mapped_column(
        Vector(384),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    source: Mapped["Source"] = relationship(
        back_populates="chunks"
    )

