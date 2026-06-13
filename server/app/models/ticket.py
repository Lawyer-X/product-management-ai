from app.db.base import Base
from sqlalchemy import String, UUID, ForeignKey, Enum as SQLEnum, DateTime, func, Text
from sqlalchemy.orm import mapped_column, Mapped, relationship
from uuid import uuid4, UUID as PyUUID
from enum import Enum
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models import Workspace

class TicketStatus(str, Enum):
    draft = "draft"
    pushed = "pushed"

class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[PyUUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    workspace_id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("workspaces.id", ondelete="CASCADE"),
        nullable=False,
    )

    workspace: Mapped["Workspace"] = relationship(
        back_populates="tickets"
    )

    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    github_issue_id: Mapped[str | None] = mapped_column(String, nullable=True)
    status: Mapped[TicketStatus] = mapped_column(SQLEnum(TicketStatus))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        onupdate=func.now()
    )