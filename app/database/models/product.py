from sqlmodel import Field, SQLModel, Column
from sqlalchemy import String
from app.database.models.base import BaseModel
from app.core.config import Currency


class Product(BaseModel, table=True):
    __tablename__ = "products"

    # id, created_at, updated_at — наследуются от BaseModel

    product_code: str = Field(
        sa_column=Column(String(10), unique=True, nullable=False),
        description="Business code, e.g. G001"
    )

    price: int = Field(
        description="Price in minor units (e.g. cents)"
    )

    currency: Currency = Field(
        description="ISO 4217 currency code"
    )
