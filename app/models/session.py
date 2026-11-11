from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime
from sqlalchemy import String, Boolean,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.db.base import Base
from typing import TYPE_CHECKING
#from app.models.message import Message
#from app.models.user import User

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.message import Message


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID (as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    title: Mapped[String] = mapped_column(
        String,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime (timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime (timezone=True),
        server_default=func.now(),
        server_onupdate=func.now(),
        nullable=False
    )

    messages: Mapped[list[Message]] = relationship(
        "Message",
        back_populates="session",
        cascade="all, delete-orphan"
    )
    user: Mapped["User"] = relationship(
        "User",
        back_populates="sessions"
    )