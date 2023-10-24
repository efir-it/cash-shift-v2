import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class PositionCheck(Base):
    """
    Модель позиции(строка) чека
    """

    __tablename__ = "positions_check"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    product_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    count: Mapped[int] = mapped_column(nullable=False, default=1)
    price: Mapped[int] = mapped_column(nullable=False, default=0)
    position: Mapped[int] = mapped_column(nullable=False)
    owner_id: Mapped[uuid.UUID] = mapped_column(nullable=False)

    check_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("checks.id", ondelete="CASCADE")
    )
    check: Mapped["Check"] = relationship(back_populates="positions")
