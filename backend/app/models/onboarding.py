from app.database.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime,Integer,ForeignKey,Text
from datetime import datetime,timezone

class OnboardingMessage(Base):
    __tablename__ = "onboarding_messages"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    agent_id: Mapped[int] = mapped_column(
        ForeignKey("agents.id"),
        nullable=False,
        index=True
    )

    role: Mapped[str] = mapped_column(
        nullable=False
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default= lambda: datetime.now(timezone.utc),
        nullable=False
    )