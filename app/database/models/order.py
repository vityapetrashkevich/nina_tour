from sqlmodel import SQLModel, Field
from app.database.models.base import BaseModel
from app.core.config import Currency


class Order(BaseModel, table=True):
    __tablename__ = "orders"

    # внешний ID от Revolut
    id: str = Field(primary_key=True)

    # тип заказа — доверяем Revolut
    type: str = Field(default="payment")

    # состояние заказа — полностью доверяем Revolut
    state: str = Field(default="pending")

    # сумма заказа
    amount: int = Field(...)

    # валюта — валидируем, потому что используем в логике
    currency: Currency = Field(...)

    # сумма, которую ещё нужно оплатить
    outstanding_amount: int = Field(default=0)

    # валюта списания — тоже валидируем
    settlement_currency: Currency = Field(...)

    # поля Revolut — не валидируем
    capture_mode: str = Field(default="automatic")
    enforce_challenge: str = Field(default="automatic")
    authorisation_type: str = Field(default="final")

    # email покупателя — можно валидировать позже
    customers_email: str = Field(...)

    # код продукта — влияет на нашу логику
    product_code: str = Field(...)

    # язык — влияет на отображение
    lang: str = Field(default="en", min_length=2, max_length=2)
