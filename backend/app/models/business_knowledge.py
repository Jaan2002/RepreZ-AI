from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, JSON,Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class BusinessKnowledge(Base):
    __tablename__ = "business_knowledge"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    agent_id: Mapped[int] = mapped_column(
        ForeignKey("agents.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True
    )

    business_name: Mapped[str | None] = mapped_column(
        nullable=True
    )

    business_type: Mapped[str | None] = mapped_column(
        nullable=True
    )

    location: Mapped[str | None] = mapped_column(
        nullable=True
    )

    description: Mapped[str | None] = mapped_column(
        nullable=True
    )

    services: Mapped[list | None] = mapped_column(
        JSON,
        nullable=True
    )

    additional_information: Mapped[str | None] = mapped_column(
        nullable=True
    )

    is_confirmed: Mapped[bool] = mapped_column(
            Boolean,
            default=False,
            nullable=False
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    