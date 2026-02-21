from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from app.core.config import Languages


class ProductCardBase(BaseModel):
    product_id: int
    lang: Languages = Field(..., example="en")
    name: str = Field(..., example="Paris Guide")
    description: str = Field(..., example="A complete guide to Paris.")


class ProductCardCreate(ProductCardBase):
    pass


class ProductCardResponse(ProductCardBase):
    id: int
    created_at: datetime
    updated_at: datetime

class ProductCardUpdate(BaseModel):
    product_id: Optional[int] = None
    lang: Optional[Languages] = None
    name: Optional[str] = None
    description: Optional[str] = None

    @field_validator("name", "description", mode="before")
    def validate_non_empty_strings(cls, v):
        if v is None:
            return v
        if isinstance(v, str) and v.strip() == "":
            raise ValueError("Поле не может быть пустой строкой")
        return v
