from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class CheckStatus(Base):
    """
    Модлель статуса чека
    """
    __tablename__ = 'check_status'

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[bool] = mapped_column(nullable=False)

    check: Mapped["Check"] = relationship(back_populates="check_status")

    def __str__(self):
        return f"type devices (id={self.id}, name=)"

    def __repr__(self):
        return str(self)
