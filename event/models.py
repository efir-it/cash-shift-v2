from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Event(Base):
    """ """

    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    status: Mapped[str] = mapped_column(nullable=False)
    queue: Mapped[str] = mapped_column(nullable=False)
    message: Mapped[str] = mapped_column(nullable=False)
    send_time: Mapped[datetime] = mapped_column(nullable=False)
