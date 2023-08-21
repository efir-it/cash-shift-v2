from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from database import Base


class Check(Base):
    """
    Модель чека
    """
    __tablename__ = 'check'

    id: Mapped[int] = mapped_column(primary_key=True)
    cash_shift_id: Mapped[int] = mapped_column(ForeignKey("cash_shift.id"))

    type_operation_id: Mapped[int] = mapped_column(ForeignKey("type_operation.id"))
    type_operation: Mapped["TypeOperation"] = relationship(back_populates="check")

    date: Mapped[datetime]
    number: Mapped[int]
    amount: Mapped[int]

    type_payment_id: Mapped[int] = mapped_column(ForeignKey("type_payment.id"))
    type_payment: Mapped["TypePayment"] = relationship(back_populates="check")

    number_fiscal_document: Mapped[int]

    check_status_id: Mapped[int] = mapped_column(ForeignKey("check_status.id"))
    check_status: Mapped["CheckStatus"] = relationship(back_populates="check")

    type_taxation_id: Mapped[int] = mapped_column(ForeignKey("type_taxation.id"))
    type_taxation: Mapped["TypeTaxation"] = relationship(back_populates="check")

    client_id: Mapped[int]

    def __str__(self):
        return f"type devices (id={self.id}, name=)"

    def __repr__(self):
        return str(self)
