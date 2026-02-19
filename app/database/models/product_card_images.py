from typing import Optional
from app.database.models.base import BaseModel
from sqlmodel import SQLModel, Field, Relationship


class ProductCardImage(BaseModel, table=True):
    __tablename__ = "product_card_images"

    product_card_id: int = Field(
        foreign_key="product_cards.id",
        index=True
    )

    file_name: str = Field(max_length=255)
    description: Optional[str] = None
    # порядок отображения
    position: int = Field(default=0)

    product_card: Optional["ProductCard"] = Relationship(
        back_populates="images"
    )
