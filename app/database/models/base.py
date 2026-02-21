from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Column
from sqlalchemy import TIMESTAMP
from sqlalchemy.sql import func


def utc_now():
    return datetime.now(timezone.utc)


class BaseModel(SQLModel, table=False):
    id: int | None = Field(default=None, primary_key=True)

    # Используем аргументы Field вместо sa_column=Column(...)
    created_at: datetime = Field(
        sa_type=TIMESTAMP(timezone=True),
        sa_column_kwargs={
            "server_default": func.now(),
            "nullable": False
        }
    )

    updated_at: datetime = Field(
        sa_type=TIMESTAMP(timezone=True),
        sa_column_kwargs={
            "server_default": func.now(),
            "onupdate": func.now(),
            "nullable": False
        }
    )
