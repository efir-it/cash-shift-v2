from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class TypePayment(Base):
    """
    Модель типа оплаты
    """

    __tablename__ = "types_payment"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    checks: Mapped["Check"] = relationship("Check")
