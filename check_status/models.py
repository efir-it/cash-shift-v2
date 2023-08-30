from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class CheckStatus(Base):
    """
    Модлель статуса чека
    """

    __tablename__ = "check_statuses"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    checks: Mapped["Check"] = relationship("Check")
