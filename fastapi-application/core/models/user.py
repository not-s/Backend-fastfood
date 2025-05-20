from datetime import date, datetime

from pydantic import EmailStr
from sqlalchemy import String, func, text, Date, Boolean
from sqlalchemy.orm import mapped_column, Mapped, relationship


from . import Base
from ..mixins.int_id_pk import IntIdMixin


class User(IntIdMixin, Base):
    email: Mapped[EmailStr] = mapped_column(String(254), unique=True)
    password: Mapped[str] = mapped_column(String(100))

    username: Mapped[str] = mapped_column(String(100), nullable=True)
    family_name: Mapped[str] = mapped_column(String(100), nullable=True)
    birthday: Mapped[date] = mapped_column(Date, nullable=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=True, unique=True)
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default=text("TRUE")
    )
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,
        server_default=func.now(),
    )



