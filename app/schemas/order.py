import re
from datetime import datetime, timezone
from pydantic import BaseModel, Field, field_validator


class OrderBase(BaseModel):
    product_code: str
    lang: str = Field(default="en")


class OrderCreate(OrderBase):
    customers_email: str = Field(example="ivan.petrov@example.com")
    settlement_currency: str = Field(min_length=3, max_length=3, description="ISO 4217 currency code in upper case",
                                     example="TRY")

    @field_validator('customers_email')
    @classmethod
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError('Email must contain @')
        return v

    @field_validator("settlement_currency")
    @classmethod
    def validate_currency(cls, v: str) -> str:
        if not v.isupper() or len(v) != 3:
            raise ValueError("Currency should be in compliance with ISO 4217 and in upper case 'EUR'")
        return v


class OrderSave(OrderCreate):
    id: str = Field(..., example="697659e8-e21b-a23f-940d-b64086ec18b2")
    token: str = Field(example="d553f7ee-fecb-431e-a4f2-8b617f3921f6", exclude=True)
    type: str = Field(example="payment")
    state: str = Field(example="pending",
                       description="State of the order (pending, processing, authorised, completed, cancelled, failed)")
    created_at: datetime = Field(..., example="2026-01-25T17:59:04.221551Z")
    updated_at: datetime = Field(..., examples="2026-01-25T17:59:04.221551Z")
    amount: int
    currency: str = Field(..., min_length=3, max_length=3, description="ISO 4217 currency code in upper case",
                          example="TRY")
    outstanding_amount: int = Field(examples=2000)
    settlement_currency: str = Field(min_length=3, max_length=3, description="ISO 4217 currency code in upper case",
                                     example="TRY")
    capture_mode: str = Field(examples="automatic")
    checkout_url: str = Field(exclude=True)
    enforce_challenge: str = Field(examples="automatic")
    authorisation_type: str = Field(examples="final")

    @field_validator("created_at", "updated_at", mode="before")
    @classmethod
    def parse_datetime(cls, v):
        if isinstance(v, str):
            # преобразуем "Z" в +00:00 и получаем aware
            return datetime.fromisoformat(v.replace("Z", "+00:00"))
        if isinstance(v, datetime) and v.tzinfo is None:
            # если naive, делаем aware UTC
            return v.replace(tzinfo=timezone.utc)
        return v
