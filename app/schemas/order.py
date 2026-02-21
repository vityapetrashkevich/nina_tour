from datetime import datetime, timezone
from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional
from app.core.config import Languages, Currency
import re


_product_code_regex = re.compile(r"^[A-Z]{1,2}\d{3,4}$")


class OrderBase(BaseModel):
    product_code: str
    lang: Languages = Field(..., example="en")



class OrderCreate(OrderBase):
    customers_email: EmailStr = Field(example="ivan.petrov@example.com")
    settlement_currency: Currency = Field(
        ...,
        description="ISO 4217 currency code",
        example="TRY"
    )

    @field_validator("product_code")
    def validate_product_code(cls, v):
        if not _product_code_regex.match(v):
            raise ValueError("product_code должен быть 1–2 заглавные буквы + 3–4 цифры")
        return v


class OrderSave(OrderBase):
    id: str = Field(..., example="697659e8-e21b-a23f-940d-b64086ec18b2")
    customers_email: EmailStr
    settlement_currency: Currency

    amount: int
    currency: Currency
    outstanding_amount: int = Field(example=2000)

    type: str = Field(example="payment")
    state: str = Field(
        example="pending",
        description="pending, processing, authorised, completed, cancelled, failed"
    )
    capture_mode: str = Field(example="automatic")
    enforce_challenge: str = Field(example="automatic")
    authorisation_type: str = Field(example="final")

    token: str = Field(exclude=True)
    checkout_url: str = Field(exclude=True)

    created_at: datetime = Field(..., example="2026-01-25T17:59:04.221551Z")
    updated_at: datetime = Field(..., example="2026-01-25T17:59:04.221551Z")

    @field_validator("created_at", "updated_at", mode="before")
    def parse_datetime(cls, v):
        if isinstance(v, str):
            return datetime.fromisoformat(v.replace("Z", "+00:00"))
        if isinstance(v, datetime) and v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v


class OrderRead(OrderBase):
    id: str = Field(..., example="697659e8-e21b-a23f-940d-b64086ec18b2")
    product_code: Optional[str] = None
    lang: Optional[Languages] = None

    # contact / payment
    customers_email: Optional[EmailStr] = None
    settlement_currency: Optional[Currency] = None

    # amounts / status
    amount: Optional[int] = None
    currency: Optional[Currency] = None
    outstanding_amount: Optional[int] = None

    type: Optional[str] = None
    state: Optional[str] = None  # pending, processing, authorised, completed, cancelled, failed
    capture_mode: Optional[str] = None
    enforce_challenge: Optional[str] = None
    authorisation_type: Optional[str] = None

    created_at: Optional[datetime]
    updated_at: Optional[datetime]


_product_code_regex = re.compile(r"^[A-Z]{1,2}\d{3,4}$")


class OrderUpdate(BaseModel):
    # from OrderBase
    product_code: Optional[str] = None
    lang: Optional[Languages] = None

    # contact / payment
    customers_email: Optional[EmailStr] = None
    settlement_currency: Optional[Currency] = None

    # amounts / status
    amount: Optional[int] = None
    currency: Optional[Currency] = None
    outstanding_amount: Optional[int] = None

    type: Optional[str] = None
    state: Optional[str] = None  # pending, processing, authorised, completed, cancelled, failed
    capture_mode: Optional[str] = None
    enforce_challenge: Optional[str] = None
    authorisation_type: Optional[str] = None

    # token and checkout_url are accepted optionally but will be ignored by CRUD (not persisted)
    token: Optional[str] = None
    checkout_url: Optional[str] = None

    # timestamps (optional on update) — created_at must not be changed by business logic,
    # updated_at is set automatically in CRUD and therefore optional here only for explicit sync cases
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @field_validator("product_code")
    def validate_product_code(cls, v):
        if v is None:
            return v
        if not _product_code_regex.match(v):
            raise ValueError("product_code должен быть 1–2 заглавные буквы + 3–4 цифры")
        return v

    @field_validator("created_at", "updated_at", mode="before")
    def parse_datetime(cls, v):
        if v is None:
            return v
        if isinstance(v, str):
            return datetime.fromisoformat(v.replace("Z", "+00:00"))
        if isinstance(v, datetime) and v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v
