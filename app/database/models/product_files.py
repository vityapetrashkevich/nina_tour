from app.database.models.base import BaseModel

from datetime import datetime, timezone
from sqlmodel import Field, Column
from sqlalchemy import String, Text, UniqueConstraint, TIMESTAMP


class ProductFile(BaseModel, table=True):
    __tablename__ = "product_files"
    __table_args__ = (
        UniqueConstraint("product_id", "lang"),
    )

    created_at: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    )

    updated_at: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    )

    product_id: int = Field(
        foreign_key="products.id",
        nullable=False
    )

    lang: str = Field(
        sa_column=Column(String(2), nullable=False),
        description="en / ru / pl"
    )

    file_link: str = Field(
        sa_column=Column(String, nullable=False),
        description="Link to downloadable file"
    )

    description: str = Field(nullable=True, description="Email message text")
