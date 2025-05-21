from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from . import Base
from core.models.mixins import IntIdPkMixin


class Token(IntIdPkMixin, Base):
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    jti: Mapped[str] = mapped_column(String(255), unique=True)