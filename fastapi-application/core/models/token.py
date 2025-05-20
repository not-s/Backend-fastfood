from datetime import date, datetime

from pydantic import EmailStr
from sqlalchemy import String, func, text, Date, Boolean, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship


from . import Base
from ..mixins.int_id_pk import IntIdMixin


class Token(IntIdMixin, Base):
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    jti: Mapped[str] = mapped_column(String(255), unique=True)