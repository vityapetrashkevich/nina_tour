from typing import Optional
from app.database.models.base import BaseModel
from datetime import datetime, timezone
from sqlmodel import Field, Column
from sqlalchemy import String, Text, UniqueConstraint, TIMESTAMP


class ProductCard(BaseModel, table=True):
    __tablename__ = "product_card"

    __table_args__ = (
        UniqueConstraint("product_id", "lang"),
    )
    created_at: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    )

    updated_at: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    )
    product_id: int = Field(foreign_key="products.id", nullable=False)
    lang: str = Field(sa_column=Column(String(2), nullable=False), description="en / ru / pl")
    name: str = Field(max_length=255, nullable=False)
    description: str = Field(sa_column=Column(Text, nullable=True))
