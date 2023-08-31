from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from database import Base


class Check(Base):
    """
    Модель чека
    """

    __tablename__ = "checks"

    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(nullable=False)
    date: Mapped[datetime] = mapped_column(nullable=False)

    number: Mapped[str] = mapped_column(nullable=False)
    amount: Mapped[int] = mapped_column(nullable=False, default=0)
    number_fiscal_document: Mapped[str] = mapped_column(nullable=False)

    cash_shift_id: Mapped[int] = mapped_column(ForeignKey("cash_shifts.id"))
    type_operation_id: Mapped[int] = mapped_column(ForeignKey("types_operation.id"))
    type_payment_id: Mapped[int] = mapped_column(ForeignKey("types_payment.id"))
    check_status_id: Mapped[int] = mapped_column(ForeignKey("check_statuses.id"))
    type_taxation_id: Mapped[int] = mapped_column(ForeignKey("types_taxation.id"))

    positions: Mapped[list["PositionCheck"]] = relationship(
        "PositionCheck",
        back_populates="check",
        cascade="all, delete",
        passive_deletes=True,
    )
