import re
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from app.core.config import Currency

from app.core.config import settings

# Регулярка для product_code: 1-2 заглавные буквы + 3 цифры
_product_code_regex = re.compile(r"^[A-Z]{1,2}\d{3,4}$")


class ProductBase(BaseModel):
    product_code: str = Field(..., example="G001")
    price: int = Field(..., description="Price in ISO 4217 minor units")
    currency: Currency = Field(..., description="ISO 4217 currency code")


class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime


class ProductCreate(ProductBase):

    @field_validator("product_code")
    def validate_product_code(cls, v: str) -> str:
        if not _product_code_regex.match(v):
            raise ValueError("product_code должен быть 1-2 заглавные буквы + 3-4 цифры, например 'G001'")
        return v


class ProductUpdate(BaseModel):
    product_code: Optional[str] = None
    price: Optional[int] = None
    currency: Optional[Currency] = None

    @field_validator("product_code", mode="before")
    def validate_product_code_update(cls, v):
        if v is None:
            return v
        if v == "":
            raise ValueError("product_code не может быть пустой строкой")
        if not _product_code_regex.match(v):
            raise ValueError("product_code должен быть 1–2 заглавные буквы + 3–4 цифры")
        return v
