from app.db.base import Base
from sqlalchemy import ForeignKey, String, DateTime, func, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID as PyUUID, uuid4
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.ticket import Ticket


class Workspace(Base):
    __tablename__ = "workspaces"

    id: Mapped[PyUUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    user_id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("auth.users.id", ondelete="CASCADE"),
        nullable=False,
    )

    tickets: Mapped[list["Ticket"]] = relationship(
        back_populates="workspace",
        cascade="all, delete-orphan",
    )

    repo_id: Mapped[str] = mapped_column(String, nullable=False)
    repo_name: Mapped[str] = mapped_column(String, nullable=False)
    project_id: Mapped[str] = mapped_column(String, nullable=False)
    project_name: Mapped[str] = mapped_column(String, nullable=False)
    context: Mapped[str] = mapped_column(Text, nullable=False)
    ai_generated_project_summary: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )