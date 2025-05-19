from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from core.mixins.int_id_pk import IntIdMixin
from . import Base


class User(IntIdMixin, Base):
    username: Mapped[str] = mapped_column(String(100), unique=True)
    email: Mapped[str] = mapped_column(String(30), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    birthday: Mapped[str]
    full_name: Mapped[str]
    phone: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow())
