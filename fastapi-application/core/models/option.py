from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from core.models import Base
from core.models.mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:

    from .option_group import OptionGroup


class Option(IntIdPkMixin, Base):
    name: Mapped[str] = mapped_column(
        String(50)
    )  # «Маленький», «Большой», «Кисло-сладкий»
    price_delta: Mapped[int] = mapped_column(
        default=0
    )  # изменение цены относительно базовой

    option_group_id: Mapped[int] = mapped_column(ForeignKey("option_groups.id"))

    option_group: Mapped["OptionGroup"] = relationship(back_populates="option")