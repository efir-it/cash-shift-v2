from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class TypeTaxation(Base):
    """
    Модель типа налогообложения
    """

    __tablename__ = "types_taxation"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    check: Mapped["Check"] = relationship("Check")
