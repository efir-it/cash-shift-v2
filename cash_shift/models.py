from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class CashShift(Base):
    """
    Модель кассовых смен
    """

    __tablename__ = "cash_shifts"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    date: Mapped[datetime] = mapped_column(nullable=False)
    organization_id: Mapped[int] = mapped_column(nullable=False)
    store_id: Mapped[int] = mapped_column(nullable=False)
    client_id: Mapped[int] = mapped_column(nullable=False)
    workplace_id: Mapped[int] = mapped_column(nullable=False)
    personal_id: Mapped[int] = mapped_column(nullable=False)
    cash_registr_id: Mapped[int] = mapped_column(nullable=False)
    status: Mapped[bool] = mapped_column(nullable=False, default=True)
    hide: Mapped[bool] = mapped_column(nullable=False, default=False)

    checks: Mapped[list["Check"]] = relationship("Check")
