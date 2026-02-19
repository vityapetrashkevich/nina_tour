from sqlmodel import Field, SQLModel
from sqlalchemy import Column, String, UniqueConstraint

class Lang(SQLModel):
    __tablename__ = 'lang'
    lang: str = Field(primary_key=True, max_length=2)
    name: str = Field(max_length=255, nullable=False)
