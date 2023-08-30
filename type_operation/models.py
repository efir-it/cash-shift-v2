from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class TypeOperation(Base):
    """
    Модель типа операции
    """

    __tablename__ = "types_operation"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    checks: Mapped["Check"] = relationship("Check")
