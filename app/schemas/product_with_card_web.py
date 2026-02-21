from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from app.schemas import ProductCardImageResponse


class ProductWithCardResponse(BaseModel):
    # Product fields (подставь реальные поля из ProductResponse, здесь минимальный набор)
    product_id: int = Field(..., example=123)
    product_code: str = Field(..., example="AB123")
    price: Optional[int] = Field(None, example=1999)
    currency: Optional[str] = Field(None, example="EUR")

    # Card fields (для конкретного языка)
    card_id: int = Field(..., example=42, description="ID карточки (product_card.id)")
    lang: str = Field(..., example="en", description="Язык карточки")
    name: str = Field(..., example="Paris Guide", description="Название карточки на данном языке")
    description: str = Field(..., example="A complete guide to Paris.", description="Описание карточки в Markdown")


    # Images related to this card
    images: List[ProductCardImageResponse] = Field(
        default_factory=list,
        description="Список изображений, относящихся к этой карточке"
    )

    class Config:
        arbitrary_types_allowed = True
