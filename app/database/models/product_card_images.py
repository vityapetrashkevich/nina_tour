from sqlmodel import SQLModel, Field, Column
from sqlalchemy import String, Text
from app.database.models.base import BaseModel


class ProductCardImage(BaseModel, table=True):
    __tablename__ = "product_card_images"

    # id, created_at, updated_at — наследуются от BaseModel

    product_card_id: int = Field(
        foreign_key="product_card.id",
        nullable=False,
        description="ID of the product card this image belongs to"
    )

    url: str = Field(
        sa_column=Column(Text, nullable=False),
        description="URL or path to the image file"
    )

    alt: str | None = Field(
        sa_column=Column(String(255), nullable=True),
        description="Alternative text for accessibility and SEO"
    )

    description: str | None = Field(
        sa_column=Column(Text, nullable=True),
        description="Optional descriptive text accompanying the image"
    )

    position: int = Field(
        default=0,
        description="Order of the image in the gallery"
    )
