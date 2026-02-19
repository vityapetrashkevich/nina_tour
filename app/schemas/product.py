import re
from pydantic import BaseModel, Field, field_validator


from app.core.config import settings

# Регулярка для product_code: 1-2 заглавные буквы + 3 цифры
_product_code_regex = re.compile(r"^[A-Z]{1,2}\d{3,4}$")

class Product(BaseModel):
    product_code: str = Field(..., example="G001", description="Business code of the product")
    # land: List[settings.Languages] = Field(..., example="en",
    #                                        description="list of languages in which the product is available")
    price: int = Field(..., description="prise unit of the product in compliance ISO 4217")
    currency: str = Field(..., min_length=3, max_length=3, description="ISO 4217 currency code in upper case")


class ProductResponse(Product):
    id: int


class ProductCreate(Product):

    @field_validator("product_code")
    def validate_product_code(cls, v: str) -> str:
        if not _product_code_regex.match(v):
            raise ValueError("product_code должен быть 1-2 заглавные буквы + 3-4 цифры, например 'G001'")
        return v

    @field_validator("currency")
    def validate_currency(cls, v: str) -> str:
        if not v.isupper() or len(v) != 3:
            raise ValueError("Currency should be in compliance with ISO 4217 and in upper case 'EUR'")
        return v
