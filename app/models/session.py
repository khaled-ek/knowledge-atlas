import uuid
from datetime import datetime, timezone

from DateTime import DateTime
from sqlalchemy import String, Boolean,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.db.base import Base
from app.models.message import Message
from app.models.user import User

class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[UUID] = mapped_column(
        UUID (as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    user_id: Mapped[UUID] = mapped_column(
        UUID (as_uuid=True),
        foreign_key="user.id",
        nullable=False,
        index=True
    )

    title: Mapped[String] = mapped_column(
        String,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime (timezone=True),
        default = lambda: datetime.now(timezone.utc),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime (timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    messages: Mapped[list["Message"]] = relationship(
        back_populates="session",
        cascade="all, delete-orphan"
    )

    user: Mapped["User"] = relationship(
        back_populates="sessions"
    )