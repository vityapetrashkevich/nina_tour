from pydantic import BaseModel, Field, HttpUrl
from app.core.config import settings
from typing import List, Optional


class ProductImage(BaseModel):
    url: HttpUrl          # ссылка на картинку
    description: Optional[str] = None


class ProductCardBase(BaseModel):
    product_id: int

    lang: settings.Languages = Field(..., example="en")
    name: str = Field(..., example="Paris Guide")
    description: str = Field(..., example="A complete guide to Paris.")
    description_html: str = Field(description='Product description with HTML tags',
                                  examples="A complete guide to Paris.")
    images: List[ProductImage] = []


class ProductCardCreate(ProductCardBase):
    pass


class ProductCardResponse(ProductCardBase):
    id: int

