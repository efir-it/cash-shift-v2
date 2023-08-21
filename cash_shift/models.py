from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class CashShift(Base):
    """
    Модель кассовых смен
    """
    __tablename__ = 'cash_shift'

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    date: Mapped[datetime]
    organization_id: Mapped[int]
    client_id: Mapped[int]
    rmk_id: Mapped[int]
    worker_id: Mapped[int]
    device_id: Mapped[int]
    status: Mapped[bool]

    check: Mapped[list["Check"]] = relationship()

    # def __str__(self):
    #     return f"contractors(" \
    #            f"id={self.id}, " \
    #            f"name={self.name}, " \
    #
    # def __repr__(self):
    #     return str(self)
