from typing import Optional, List
from app.database.models.base import BaseModel
from datetime import datetime, timezone

from sqlmodel import SQLModel, Field, Column
from sqlalchemy import Column, String, TIMESTAMP


class Product(SQLModel, table=True):
    __tablename__ = "products"

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    )
    updated_at: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    )
    product_code: str = Field(
        sa_column=Column(String(10), unique=True, nullable=False),
        description="Business code, e.g. G001"
    )
    # langs: List[str] = Field(description="list of languages in which the product is available")

    price: int = Field(description="Price in minor units (e.g. cents)")

    currency: str = Field(
        sa_column=Column(String(3), nullable=False),
        description="ISO 4217, uppercase"
    )

