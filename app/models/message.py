import uuid
from datetime import datetime, timezone

from DateTime import DateTime
from sqlalchemy import String, Boolean, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB

from app.db.base import Base
from app.models.session import Session

class Message(Base):
    __tablename__ = "messages"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default = uuid.uuid4()
    )

    source_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("Session.id"),
        index = True
    )

    role: Mapped[str] = relationship(
        String(20),
        nullable = False
    )

    content: Mapped[str] = relationship(
        String,
        nullable = False
    )

    created_at: Mapped[datetime] = relationship(
        DateTime(timezone=True),
        default = lambda: datetime.now(timezone.utc),
        nullable = False
    )

    session: Mapped["Session"] = relationship(
        back_populates="messages"
    )