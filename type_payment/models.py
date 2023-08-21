from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class TypePayment(Base):
    """
    Модель типа оплаты
    """
    __tablename__ = 'type_payment'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    check: Mapped["Check"] = relationship(back_populates="type_payment")

    def __str__(self):
        return f"type devices (id={self.id}, name={self.name})"

    def __repr__(self):
        return str(self)
