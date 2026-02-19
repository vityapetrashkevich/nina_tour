from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Column
from sqlalchemy import TIMESTAMP
import sqlalchemy as sa

def utc_now():
    """Функция для default_factory — всегда возвращает aware datetime UTC"""
    return datetime.now(timezone.utc)


class BaseModel(SQLModel):
    id: int = Field(default=None, primary_key=True)
    created_at: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    )

    updated_at: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    )