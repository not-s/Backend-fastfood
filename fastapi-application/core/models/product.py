from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, func, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base
from core.models.mixins import IntIdPkMixin
if TYPE_CHECKING:
    from .cart_food_association import CartFoodAssociation
    from .category import Category
    from .option_group import OptionGroup



class Product(IntIdPkMixin, Base):
    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[int]
    image_url: Mapped[str] = mapped_column(String(255))
    weight_g: Mapped[int | None]
    volume_ml: Mapped[int | None]
    stock: Mapped[int] = mapped_column(default=0, server_default="0")
    is_available: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow(), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow(), server_default=func.now()
    )

    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))

    category: Mapped["Category"] = relationship(back_populates="products")
    carts_details: Mapped[list["CartFoodAssociation"]] = relationship(
        back_populates="products"
    )
    option_group: Mapped[list["OptionGroup"]] = relationship(back_populates="products")