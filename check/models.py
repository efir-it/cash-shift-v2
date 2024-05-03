import uuid
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Receipt(Base):
    """
    Модель чека
    """

    __tablename__ = "checks"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    owner_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    organization_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    store_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    reasonCheckName: Mapped[str] = mapped_column(default='', nullable=True)
    date: Mapped[datetime] = mapped_column(nullable=False)
    number: Mapped[str] = mapped_column(nullable=True)
    amount: Mapped[int] = mapped_column(nullable=False, default=0)
    number_fiscal_document: Mapped[str] = mapped_column(nullable=True)
    reason_id: Mapped[uuid.UUID] = mapped_column(nullable=True)
    workplace_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    
    cash_shift_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("cash_shifts.id"))
    cash_shift: Mapped["CashShift"] = relationship(back_populates="checks")

    type_operation: Mapped[int] = mapped_column(nullable=False)
    type_payment: Mapped[int] = mapped_column(nullable=False)
    check_status: Mapped[int] = mapped_column(nullable=False)
    type_taxation: Mapped[int] = mapped_column(nullable=False)

    positions: Mapped[list["PositionCheck"]] = relationship(
        back_populates="check",
        cascade="all, delete",
        passive_deletes=True,
    )
