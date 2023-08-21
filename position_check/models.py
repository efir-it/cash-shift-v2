from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from database import Base


class PositionCheck(Base):
    """
    Модель позиции(строка) чека
    """
    __tablename__ = 'position_check'

    id: Mapped[int] = mapped_column(primary_key=True)
    check_id: Mapped[int] = mapped_column(ForeignKey("check.id"))
    product_id: Mapped[int]
    count: Mapped[int]
    price: Mapped[int]
    position: Mapped[int]
    client_id: Mapped[int]

    def __str__(self):
        return f"type devices (id={self.id}, name=)"

    def __repr__(self):
        return str(self)
