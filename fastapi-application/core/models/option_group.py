from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from core.models import Base
from core.models.mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from .product import Product
    from .option import Option


#  Дополнительные группы. Например, соусы и добавки
class OptionGroup(IntIdPkMixin, Base):
    name: Mapped[str] = mapped_column(String(50))
    required: Mapped[bool] = mapped_column(default=False)

    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))

    products: Mapped["Product"] = relationship(back_populates="option_group")
    option: Mapped[list["Option"]] = relationship(back_populates="option_group")