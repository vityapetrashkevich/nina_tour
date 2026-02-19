from datetime import datetime, timezone
from sqlmodel import Field, Column, SQLModel
from sqlalchemy import String, Text, UniqueConstraint, TIMESTAMP




# class Order(Base):
#     __tablename__ = "orders"
#
#     id = Column(String, primary_key=True, index=True)
#     type = Column(String, default="payment", nullable=False)
#     state = Column(String, default="pending", nullable=False,
#                    comment="State of the order (pending, processing, authorised, completed, cancelled, failed)")
#     created_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
#     updated_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
#     amount = Column(Integer, nullable=False)
#     currency = Column(String(3), nullable=False, comment="ISO 4217 currency code in upper case")
#     outstanding_amount = Column(Integer, default=0)
#     settlement_currency = Column(String(3), nullable=False, comment="ISO 4217 currency code in upper case")
#     capture_mode = Column(String, default="automatic")
#     enforce_challenge = Column(String, default="automatic")
#     authorisation_type = Column(String, default="final")
#     product_code = Column(String, comment="business product code")
#     lang = Column(String)
#     customers_email = Column(String, nullable=False)

class Order(SQLModel, table=True):
    __tablename__ = "orders"  # имя таблицы в БД

    id: str = Field(primary_key=True)
    type: str = Field(default="payment")
    state: str = Field(default="pending",
                       description="State of the order (pending, processing, authorised, completed, cancelled, failed)")
    created_at: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    )

    updated_at: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    )
    amount: int = Field(...)
    currency: str = Field(..., min_length=3, max_length=3, description="ISO 4217 currency code in upper case")
    outstanding_amount: int = Field(default=0)
    settlement_currency: str = Field(min_length=3, max_length=3, description="ISO 4217 currency code in upper case")
    capture_mode: str = Field(default="automatic")
    enforce_challenge: str = Field(default="automatic")
    authorisation_type: str = Field(default="final")
    customers_email: str = Field(...)
    product_code: str = Field(...)
    lang: str
