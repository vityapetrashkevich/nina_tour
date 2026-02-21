from sqlmodel import Field, Column
from sqlalchemy import String, Text, UniqueConstraint
from app.database.models.base import BaseModel


class ProductFile(BaseModel, table=True):
    __tablename__ = "product_files"

    __table_args__ = (
        UniqueConstraint("product_id", "lang"),
    )

    # id, created_at, updated_at — наследуются от BaseModel

    product_id: int = Field(
        foreign_key="products.id",
        nullable=False,
        description="ID of the product this file belongs to"
    )

    lang: str = Field(
        sa_column=Column(String(2), nullable=False),
        description="Language code: en / ru / pl"
    )

    file_link: str = Field(
        sa_column=Column(Text, nullable=False),
        description="Direct link to downloadable guide file"
    )

    description: str | None = Field(
        sa_column=Column(Text, nullable=True),
        description="Optional text used in email body when sending the file"
    )
