from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


# Общие поля для всех схем
class ProductCardImageBase(BaseModel):
    product_card_id: int
    file_name: str = Field(..., max_length=255)
    description: Optional[str] = None
    position: int = 0


# Схема для создания (POST) — id и даты не передаются клиентом
class ProductCardImageCreate(ProductCardImageBase):
    pass


# Схема для чтения (GET) — включает все поля из БД
class ProductCardImageRead(ProductCardImageBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)