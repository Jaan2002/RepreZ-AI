from app.database.base import Base
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import Integer,DateTime,String

from datetime import datetime,timezone


class Agent(Base):
    __tablename__="agents"

    id: Mapped[int]= mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    business_name: Mapped[str]= mapped_column(
        String(100),
        nullable=False
    )
    status: Mapped[str]= mapped_column(
        String(50),
        default="learning",
        nullable=False
    )

    created_at: Mapped[datetime]= mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )