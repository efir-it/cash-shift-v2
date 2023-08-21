from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class TypeTaxation(Base):
    """
    Модлель типа налогообложения
    """
    __tablename__ = 'type_taxation'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    check: Mapped["Check"] = relationship(back_populates="type_taxation")

    def __str__(self):
        return f"type devices (id={self.id}, name={self.name})"

    def __repr__(self):
        return str(self)
