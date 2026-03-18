from sqlmodel import SQLModel, Field
from app.database.models.base import BaseModel


class Admin(BaseModel, table=True):
    email: str = Field(..., unique=True,)
    password_hash: str = Field(...)
    public_key_pem: str = Field(...)
    is_active: bool = Field(default=True)
