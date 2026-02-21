from sqlmodel import SQLModel, Field, Column
from sqlalchemy import String, Text, UniqueConstraint
from app.database.models.base import BaseModel
from app.core.config import Languages


class ProductCard(BaseModel, table=True):
    __tablename__ = "product_card"

    __table_args__ = (
        UniqueConstraint("product_id", "lang"),
    )

    # id, created_at, updated_at — наследуются от BaseModel

    product_id: int = Field(
        foreign_key="products.id",
        nullable=False
    )

    lang: Languages = Field(
        nullable=False,
        description="Language code: en / ru / pl"
    )

    name: str = Field(
        max_length=255,
        nullable=False
    )

    description: str | None = Field(
        sa_column=Column(Text, nullable=True),
        description="Localized product description in Markdown format"
    )
