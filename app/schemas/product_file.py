from pydantic import BaseModel, Field
from app.core.config import settings

class ProductFile(BaseModel):
    lang: settings.Languages = Field(..., example="en")
    file_link: str = Field(..., example="https://bucket.s3/guide_en.pdf")