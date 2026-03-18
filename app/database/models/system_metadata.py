from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Column
from sqlalchemy import TIMESTAMP
from sqlalchemy.sql import func


class SystemMetadata(SQLModel, table=True):
    key: str = Field(primary_key=True)
    value: str
    updated_at: datetime = Field(
        sa_type=TIMESTAMP(timezone=True),
        sa_column_kwargs={
            "server_default": func.now(),
            "onupdate": func.now(),
            "nullable": False
        }
    )
