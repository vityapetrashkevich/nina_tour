from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field, field_validator

from app.core.config import Languages


# -------------------------
# 1. BASE
# -------------------------
class ProductFileBase(BaseModel):
    file_link: str = Field(..., example="/downloads/guides/paris_en.pdf", description="Direct link or path to downloadable file")
    description: Optional[str] = Field(None, example="File sent to customer after purchase")

    @field_validator("file_link", mode="before")
    def validate_file_link(cls, v: str) -> str:
        if v is None:
            raise ValueError("file_link is required")
        if not isinstance(v, str) or v.strip() == "":
            raise ValueError("file_link не может быть пустой строкой")
        if " " in v:
            raise ValueError("file_link не должен содержать пробелов")
        lower = v.lower()
        # allow http(s) URLs or server paths (absolute or relative)
        if lower.startswith("http://") or lower.startswith("https://"):
            return v
        # disallow other schemes like ftp:, data:, etc.
        if ":" in v.split("/")[0]:
            raise ValueError("file_link должен быть либо http(s) URL, либо путём на сервере без схемы")
        return v

    @field_validator("description", mode="before")
    def validate_description(cls, v):
        if v is None:
            return v
        if isinstance(v, str) and v.strip() == "":
            raise ValueError("description не может быть пустой строкой")
        return v


# -------------------------
# 2. CREATE
# -------------------------
class ProductFileCreate(ProductFileBase):
    product_id: int = Field(..., example=123, description="ID of the product this file belongs to")
    lang: Languages = Field(..., example="en", description="Language code (2 letters)")


# -------------------------
# 3. UPDATE
# -------------------------
class ProductFileUpdate(BaseModel):
    file_link: Optional[str] = None
    description: Optional[str] = None
    lang: Optional[Languages] = None

    @field_validator("file_link", mode="before")
    def validate_file_link_update(cls, v):
        if v is None:
            return v
        if not isinstance(v, str) or v.strip() == "":
            raise ValueError("file_link не может быть пустой строкой")
        if " " in v:
            raise ValueError("file_link не должен содержать пробелов")
        lower = v.lower()
        if lower.startswith("http://") or lower.startswith("https://"):
            return v
        if ":" in v.split("/")[0]:
            raise ValueError("file_link должен быть либо http(s) URL, либо путём на сервере без схемы")
        return v

    @field_validator("description", mode="before")
    def validate_description_update(cls, v):
        if v is None:
            return v
        if isinstance(v, str) and v.strip() == "":
            raise ValueError("description не может быть пустой строкой")
        return v


# -------------------------
# 4. RESPONSE
# -------------------------
class ProductFileResponse(ProductFileBase):
    id: int = Field(..., example=1)
    product_id: int = Field(..., example=123)
    lang: Languages = Field(..., example="en")
    created_at: datetime = Field(..., example="2026-01-25T17:59:04.221551Z")
    updated_at: datetime = Field(..., example="2026-01-25T17:59:04.221551Z")

    @field_validator("created_at", "updated_at", mode="before")
    def parse_datetime(cls, v):
        if isinstance(v, str):
            return datetime.fromisoformat(v.replace("Z", "+00:00"))
        if isinstance(v, datetime) and v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v
