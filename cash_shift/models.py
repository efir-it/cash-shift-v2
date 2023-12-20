import uuid
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class CashShift(Base):
    """
    Модель кассовых смен
    """

    __tablename__ = "cash_shifts"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    date: Mapped[datetime] = mapped_column(nullable=False)
    organization_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    store_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    owner_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    workplace_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    worker_id: Mapped[uuid.UUID] = mapped_column(nullable=True)
    cash_registr_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    closed: Mapped[bool] = mapped_column(nullable=False, default=False)
    hide: Mapped[bool] = mapped_column(nullable=False, default=False)

    checks: Mapped[list["Receipt"]] = relationship(back_populates="cash_shift")
