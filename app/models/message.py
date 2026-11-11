from __future__ import annotations

import uuid

from sqlalchemy import String, Text, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
from typing import TYPE_CHECKING
from sqlalchemy.sql import func


from app.db.base import Base#from app.models.session import Session

if TYPE_CHECKING:
    from app.models.session import ChatSession

class Message(Base):
    __tablename__ = "messages"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default = uuid.uuid4
    )

    session_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("chat_sessions.id"),
        index = True
    )

    role: Mapped[str] = mapped_column(
        String(20),
        nullable = False
    )

    content: Mapped[str] = mapped_column(
        String,
        nullable = False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable = False
    )

    session: Mapped["ChatSession"] = relationship(
        "ChatSession",
        back_populates="messages"
    )