from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field, field_validator, ValidationError


# -------------------------
# 1. BASE
# -------------------------
class ProductCardImageBase(BaseModel):
    url: str = Field(..., example="/uploads/images/cover.jpg", description="Path to image on server")
    alt: Optional[str] = Field(None, max_length=255, example="Front cover", description="Alternative text for accessibility")
    description: Optional[str] = Field(None, example="High resolution front cover image")
    position: int = Field(0, description="Order of the image in the gallery", example=0)

    @field_validator("url", mode="before")
    def validate_url(cls, v: str) -> str:
        if v is None:
            raise ValueError("url is required")
        if not isinstance(v, str) or v.strip() == "":
            raise ValueError("url не может быть пустой строкой")
        if " " in v:
            raise ValueError("url не должен содержать пробелов")
        lower = v.lower()
        if lower.startswith("http://") or lower.startswith("https://") or ":" in v.split("/")[0]:
            raise ValueError("url должен быть путем на сервере, без схемы (http/https)")
        return v

    @field_validator("alt", "description", mode="before")
    def non_empty_strings(cls, v):
        if v is None:
            return v
        if isinstance(v, str) and v.strip() == "":
            raise ValueError("Поле не может быть пустой строкой")
        return v

    @field_validator("position")
    def position_non_negative(cls, v):
        if not isinstance(v, int):
            raise ValueError("position должен быть целым числом")
        if v < 0:
            raise ValueError("position не может быть отрицательным")
        return v


# -------------------------
# 2. CREATE
# -------------------------
class ProductCardImageCreate(ProductCardImageBase):
    product_card_id: int = Field(..., example=42, description="ID of the product card this image belongs to")


# -------------------------
# 3. UPDATE
# -------------------------
class ProductCardImageUpdate(BaseModel):
    url: Optional[str] = None
    alt: Optional[str] = None
    description: Optional[str] = None
    position: Optional[int] = None

    @field_validator("url", mode="before")
    def validate_url_update(cls, v):
        if v is None:
            return v
        if not isinstance(v, str) or v.strip() == "":
            raise ValueError("url не может быть пустой строкой")
        if " " in v:
            raise ValueError("url не должен содержать пробелов")
        return v

    @field_validator("alt", "description", mode="before")
    def non_empty_strings_update(cls, v):
        if v is None:
            return v
        if isinstance(v, str) and v.strip() == "":
            raise ValueError("Поле не может быть пустой строкой")
        return v

    @field_validator("alt")
    def alt_max_length_update(cls, v):
        if v is None:
            return v
        if len(v) > 255:
            raise ValueError("alt не может быть длиннее 255 символов")
        return v

    @field_validator("position")
    def position_non_negative_update(cls, v):
        if v is None:
            return v
        if not isinstance(v, int):
            raise ValueError("position должен быть целым числом")
        if v < 0:
            raise ValueError("position не может быть отрицательным")
        return v


# -------------------------
# 4. RESPONSE
# -------------------------
class ProductCardImageResponse(ProductCardImageBase):
    id: int = Field(..., example=1)
    product_card_id: int = Field(..., example=42)
    created_at: datetime = Field(..., example="2026-01-25T17:59:04.221551Z")
    updated_at: datetime = Field(..., example="2026-01-25T17:59:04.221551Z")

    @field_validator("created_at", "updated_at", mode="before")
    def parse_datetime(cls, v):
        if isinstance(v, str):
            return datetime.fromisoformat(v.replace("Z", "+00:00"))
        if isinstance(v, datetime) and v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v
