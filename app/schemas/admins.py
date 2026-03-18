from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional
from datetime import datetime


class AdminBase(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime


class AdminRegisterRequest(BaseModel):
    email: EmailStr
    public_key: str = Field(
        description="Публичный ключ клиента в PEM или Base64 формате"
    )


class AdminRegisterResponse(AdminBase):
    email: EmailStr
    password: str
    message: str = "Client registered successfully"


class AdminRead(AdminBase):
    email: EmailStr
    public_key: str
    is_active: bool


class StepUpRequest(BaseModel):
    email: EmailStr
    password: str


class StepUpResponse(AdminBase):
    access_token: str
    token_type: str = "bearer"



class AdminUpdateRequest(BaseModel):
    id: Optional[int]
    password: Optional[str] = Field(
        default=None,
        min_length=8,
        description="Новый пароль клиента"
    )
    public_key: Optional[str] = Field(
        default=None,
        description="Новый публичный ключ клиента в PEM или Base64 формате"
    )

    @field_validator("public_key")
    def validate_public_key(cls, v):
        if v is None:
            return v
        # Простая проверка на PEM‑формат (не строгая)
        if "BEGIN PUBLIC KEY" not in v:
            raise ValueError("Публичный ключ должен быть в PEM формате")
        return v


class AdminUpdateResponse(AdminBase):
    email: EmailStr
    public_key: str
    is_active: bool
    message: str = "Client updated successfully"
