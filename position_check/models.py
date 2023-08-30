from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from database import Base


class PositionCheck(Base):
    """
    Модель позиции(строка) чека
    """

    __tablename__ = "positions_check"

    id: Mapped[int] = mapped_column(primary_key=True)

    product_id: Mapped[int] = mapped_column(nullable=False)
    count: Mapped[int] = mapped_column(nullable=False, default=1)
    price: Mapped[int] = mapped_column(nullable=False, default=0)
    position: Mapped[int] = mapped_column(nullable=False)
    client_id: Mapped[int] = mapped_column(nullable=False)

    check_id: Mapped[int] = mapped_column(ForeignKey("checks.id"))
